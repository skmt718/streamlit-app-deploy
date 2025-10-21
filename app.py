import streamlit as st
from typing import Tuple, Optional


# 定数定義
BMI_UNDERWEIGHT = 18.5
BMI_NORMAL = 25.0
BMI_OVERWEIGHT = 30.0
MAX_HEIGHT = 300
MAX_WEIGHT = 1000


def calculate_bmi(height: float, weight: float) -> float:
    """BMI値を計算する
    
    Args:
        height: 身長（cm）
        weight: 体重（kg）
    
    Returns:
        BMI値
    """
    return weight / ((height / 100) ** 2)


def get_bmi_category(bmi: float) -> Tuple[str, str]:
    """BMI値から判定結果とメッセージタイプを取得する
    
    Args:
        bmi: BMI値
        
    Returns:
        判定結果とメッセージタイプのタプル (判定結果, メッセージタイプ)
    """
    if bmi < BMI_UNDERWEIGHT:
        return "判定: 低体重", "info"
    elif bmi < BMI_NORMAL:
        return "判定: 普通体重", "success"
    elif bmi < BMI_OVERWEIGHT:
        return "判定: 肥満（1度）", "warning"
    else:
        return "判定: 肥満（2度以上）", "error"


def validate_inputs(height: str, weight: str) -> Optional[Tuple[float, float]]:
    """入力値の妥当性をチェックし、変換された値を返す
    
    Args:
        height: 身長の文字列
        weight: 体重の文字列
        
    Returns:
        変換された身長と体重のタプル、またはNone（エラーの場合）
    """
    try:
        height_float = float(height)
        weight_float = float(weight)
        
        if height_float <= 0 or weight_float <= 0:
            st.error("身長と体重は正の数値で入力してください。")
            return None
        elif height_float > MAX_HEIGHT or weight_float > MAX_WEIGHT:
            st.error("身長と体重の値が範囲外です。適切な値を入力してください。")
            return None
        
        return height_float, weight_float
        
    except ValueError:
        st.error("身長と体重は数値で入力してください。")
        return None


def display_text_counter(text: str) -> None:
    """文字数カウント結果を表示する
    
    Args:
        text: カウント対象のテキスト
    """
    if text:
        text_count = len(text)
        st.write(f"文字数: **{text_count}**")
    else:
        st.error("カウント対象となるテキストを入力してから「実行」ボタンを押してください。")


def display_bmi_result(height: str, weight: str) -> None:
    """BMI計算結果を表示する
    
    Args:
        height: 身長の文字列
        weight: 体重の文字列
    """
    if not height or not weight:
        st.error("身長と体重をどちらも入力してください。")
        return
    
    validated_inputs = validate_inputs(height, weight)
    if validated_inputs is None:
        return
    
    height_float, weight_float = validated_inputs
    bmi = calculate_bmi(height_float, weight_float)
    st.write(f"BMI値: **{bmi:.1f}**")
    
    category, message_type = get_bmi_category(bmi)
    
    # メッセージタイプに応じた表示
    if message_type == "info":
        st.info(category)
    elif message_type == "success":
        st.success(category)
    elif message_type == "warning":
        st.warning(category)
    else:
        st.error(category)


def render_header() -> None:
    """ヘッダー部分を表示する"""
    st.title("サンプルアプリ②: 少し複雑なWebアプリ")
    st.write("#### 動作モード1: 文字数カウント")
    st.write("入力フォームにテキストを入力し、「実行」ボタンを押すことで文字数をカウントできます。")
    st.write("##### 動作モード2: BMI値の計算")
    st.write("身長と体重を入力することで、肥満度を表す体型指数のBMI値を算出できます。")


def get_input_values(selected_mode: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """選択されたモードに応じた入力値を取得する
    
    Args:
        selected_mode: 選択されたモード
        
    Returns:
        (input_message, height, weight) のタプル
    """
    if selected_mode == "文字数カウント":
        input_message = st.text_input(
            label="文字数のカウント対象となるテキストを入力してください。",
            placeholder="例: こんにちは、世界！"
        )
        return input_message, None, None
    else:
        height = st.text_input(
            label="身長（cm）を入力してください。",
            placeholder="例: 170.5"
        )
        weight = st.text_input(
            label="体重（kg）を入力してください。",
            placeholder="例: 65.0"
        )
        return None, height, weight


def main() -> None:
    """メイン処理"""
    render_header()
    
    selected_item = st.radio(
        "動作モードを選択してください。",
        ["文字数カウント", "BMI値の計算"]
    )
    
    st.divider()
    
    input_message, height, weight = get_input_values(selected_item)
    
    if st.button("実行"):
        st.divider()
        
        if selected_item == "文字数カウント":
            display_text_counter(input_message)
        else:
            display_bmi_result(height, weight)


if __name__ == "__main__":
    main()
