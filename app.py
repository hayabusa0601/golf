import streamlit as st
from quiz_manager import QuizManager
from quiz_data import quiz_data

def initialize_session_state():
    """セッション状態の初期化"""
    if 'quiz_manager' not in st.session_state:
        st.session_state.quiz_manager = None
    if 'current_difficulty' not in st.session_state:
        st.session_state.current_difficulty = None
    if 'show_explanation' not in st.session_state:
        st.session_state.show_explanation = False

def display_score_evaluation(accuracy: float):
    """スコアに基づく評価の表示"""
    if accuracy >= 80:
        st.balloons()
        st.markdown("### 🏆 素晴らしい成績です！")
        st.write("ゴルフルールをよく理解していますね！")
    elif accuracy >= 60:
        st.markdown("### 📚 よく頑張りました！")
        st.write("基本的なルールは理解できています。")
    else:
        st.markdown("### 💪 もう少し練習しましょう！")
        st.write("基本的なルールから復習していきましょう。")

def display_answer_result(option, correct_answer, selected_option, is_correct):
    """選択肢の結果表示"""
    if option == selected_option:
        if is_correct:
            return f"✅ {option}"
        else:
            return f"❌ {option}"
    elif option == correct_answer and not is_correct:
        return f"⭕ {option} (正解)"
    else:
        return option

def main():
    st.set_page_config(
        page_title="ゴルフルールクイズ",
        page_icon="⛳",
        layout="centered"
    )
    
    initialize_session_state()
    
    # ヘッダー部分
    st.title("⛳ ゴルフルールクイズ")
    st.markdown("---")
    
    # 難易度選択画面
    if st.session_state.quiz_manager is None:
        st.markdown("### 🎯 難易度と問題数を選択")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            difficulty = st.selectbox(
                "難易度を選択してください：",
                ["やさしい", "ふつう", "むずかしい"],
                help="各難易度に応じた問題が出題されます。"
            )
        
        # 選択された難易度の利用可能な問題数を取得
        available_questions = len(quiz_data[difficulty])
        with col2:
            num_questions = st.number_input(
                "問題数：",
                min_value=1,
                max_value=available_questions,
                value=5,
                help=f"1-{available_questions}問の範囲で選択できます"
            )
        
        with col3:
            if st.button("クイズを始める", type="primary", use_container_width=True):
                st.session_state.quiz_manager = QuizManager(difficulty, num_questions=int(num_questions))
                st.session_state.current_difficulty = difficulty
                st.rerun()
        
        # 問題数の表示を追加
        st.markdown(f"**選択された難易度の利用可能な問題数**: {available_questions}問")
        
        # 難易度の説明
        st.markdown("#### 難易度について")
        st.markdown("""
        - **やさしい**: ゴルフの基本的なルールに関する問題
        - **ふつう**: より詳細なルールや一般的な状況の問題
        - **むずかしい**: 特殊な状況や複雑なルールに関する問題
        """)
        
    # クイズ画面
    if st.session_state.quiz_manager is not None:
        quiz_manager = st.session_state.quiz_manager
        current_question = quiz_manager.get_current_question()
        
        # 問題が残っている場合
        if current_question is not None:
            # プログレスバーと状況表示
            progress = quiz_manager.get_progress()
            st.progress(progress[0] / progress[1])
            st.markdown(f"**難易度**: {st.session_state.current_difficulty}")
            st.markdown(f"**進捗**: 問題 {progress[0]}/{progress[1]}")
            
            # 問題文の表示
            st.markdown("---")
            st.markdown(f"### Q. {current_question.question}")
            
            # 選択肢の表示
            if not st.session_state.show_explanation:
                cols = st.columns(1)  # 1列でボタンを配置
                for option in current_question.options:
                    if st.button(option, key=option, use_container_width=True):
                        is_correct = quiz_manager.check_answer(option)
                        if is_correct:
                            st.success("🎉 正解です！")
                        else:
                            st.error("😢 不正解です。")
                        st.session_state.show_explanation = True
                        st.rerun()
            
            # 解説の表示
            if st.session_state.show_explanation:
                result = quiz_manager.get_last_result()
                st.markdown("#### 選択肢:")
                for option in current_question.options:
                    display_text = display_answer_result(
                        option, 
                        current_question.correct_answer,
                        result["selected_option"],
                        result["is_correct"]
                    )
                    st.markdown(f"- {display_text}")
                
                st.markdown("#### 解説")
                st.info(current_question.explanation)
                
                # 最終問題の場合は「結果を確認」、それ以外は「次の問題へ」を表示
                if quiz_manager.get_progress()[0] == quiz_manager.get_progress()[1]:
                    if st.button("結果を確認", type="primary", use_container_width=True):
                        quiz_manager.next_question()
                        st.session_state.show_explanation = False
                        st.rerun()
                else:
                    if st.button("次の問題へ", type="primary", use_container_width=True):
                        quiz_manager.next_question()
                        st.session_state.show_explanation = False
                        st.rerun()
        
        # クイズ終了時の表示
        else:
            st.markdown("---")
            st.markdown("### 🎊 クイズ完了！")
            
            # スコアの表示
            score = quiz_manager.get_score()
            accuracy = (score[0] / score[1]) * 100
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("正解数", f"{score[0]}/{score[1]}")
            with col2:
                st.metric("正答率", f"{accuracy:.1f}%")
            
            # 評価の表示
            display_score_evaluation(accuracy)
            
            # リスタートボタン
            st.markdown("---")
            if st.button("ホーム画面に戻る", type="primary", use_container_width=True):
                st.session_state.quiz_manager = None
                st.session_state.current_difficulty = None
                st.session_state.show_explanation = False
                st.rerun()

if __name__ == "__main__":
    main()