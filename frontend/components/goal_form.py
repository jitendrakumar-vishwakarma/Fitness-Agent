"""
Goal form component
"""

import streamlit as st


def render_goal_form():
    """Render the goal setting form"""

    st.title("🎯 Set Your Fitness Goals")

    # Load current goal if exists
    try:
        current_goal = st.session_state.api_client.get_goal(
            user_id=st.session_state.user_id
        )
    except:
        current_goal = None

    with st.form("goal_form"):
        st.subheader("Your Fitness Goal")

        goal_type = st.selectbox(
            "Goal Type",
            ["weight_loss", "muscle_gain", "maintenance"],
            index=(
                0
                if not current_goal
                else ["weight_loss", "muscle_gain", "maintenance"].index(
                    current_goal.get("goal_type", "maintenance")
                )
            ),
        )

        col1, col2 = st.columns(2)

        with col1:
            target_calories = st.number_input(
                "Target Daily Calories",
                min_value=1000,
                max_value=5000,
                value=(
                    current_goal.get("target_calories", 2000) if current_goal else 2000
                ),
                step=100,
            )

        with col2:
            target_weight = st.number_input(
                "Target Weight (kg)",
                min_value=30.0,
                max_value=200.0,
                value=(
                    float(current_goal.get("target_weight", 70.0))
                    if current_goal and current_goal.get("target_weight")
                    else 70.0
                ),
                step=0.5,
            )

        target_date = st.date_input("Target Date (optional)")

        submitted = st.form_submit_button("Save Goal")

        if submitted:
            try:
                response = st.session_state.api_client.set_goal(
                    user_id=st.session_state.user_id,
                    goal_type=goal_type,
                    target_calories=target_calories,
                    target_weight=target_weight,
                    target_date=str(target_date) if target_date else None,
                )

                st.success("✅ Goal saved successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error saving goal: {str(e)}")

    # Display current goal
    if current_goal:
        st.markdown("---")
        st.subheader("Current Goal")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Goal Type", current_goal["goal_type"].replace("_", " ").title())

        with col2:
            st.metric("Target Calories", f"{current_goal['target_calories']} cal/day")

        with col3:
            if current_goal.get("target_weight"):
                st.metric("Target Weight", f"{current_goal['target_weight']} kg")
