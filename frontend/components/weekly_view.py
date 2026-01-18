"""
Weekly summary view component
"""

import streamlit as st


def render_weekly_summary():
    """Render the weekly summary view"""

    st.title("📊 Your Fitness Summary")

    # Period selector
    period = st.selectbox("Select Period", ["daily", "weekly", "monthly"], index=1)

    # Fetch summary
    try:
        summary = st.session_state.api_client.get_summary(
            user_id=st.session_state.user_id, period=period
        )

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Avg Calories",
                f"{summary['avg_calories']:.0f}",
                delta=f"{summary['avg_calories'] - summary['target_calories']:.0f} vs target",
            )

        with col2:
            st.metric("Days Logged", summary["days_logged"])

        with col3:
            st.metric("Goal Adherence", f"{summary['goal_adherence']:.0f}%")

        with col4:
            st.metric("Total Calories", f"{summary['total_calories']:,}")

        # Progress bar
        st.markdown("---")
        st.subheader("Goal Progress")

        progress = min(1.0, summary["goal_adherence"] / 100)
        st.progress(progress)

        # Insights
        st.markdown("---")
        st.subheader("Insights")
        st.info(summary["insights"])

    except Exception as e:
        st.error(f"❌ Error loading summary: {str(e)}")
        st.info("Start logging your meals to see your summary!")
