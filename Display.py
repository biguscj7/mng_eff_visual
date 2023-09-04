import streamlit as st
import plotly.graph_objects as go
import pandas as pd

RED = "rgb(159,31,49)"
YELLOW = "rgb(246,205,84)"
GREEN = "rgb(128,153,42)"

st.set_page_config(page_title="2023 Rev assessment", layout="wide")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.header("2023 Revenue Unlikely to Meet Goal")

agg_data = pd.read_csv("revenue.csv", index_col="month")
individual_data = pd.read_csv("rev_by_month.csv", index_col="month")

col1, col2, col3, col4 = st.columns(4)

linear = col1.checkbox("Trendline to goal", value=True)
cum_21 = col2.checkbox("2021", value=False)
cum_22 = col3.checkbox("2022", value=False)
cum_23 = col4.checkbox("2023", value=True)

fig = go.Figure()

annotations = []

if linear:
    trace_name = "trendline to goal"
    fig.add_trace(
        go.Scatter(x=agg_data.index, y=agg_data["linear"], mode="lines", line=dict(color="gray", dash="dash"),
                   meta=[trace_name]))
    annotations.append(dict(x="Feb", y=0.167, axref="pixel", ayref="pixel",
                            ax=0, ay=-50,
                            xanchor='center', yanchor='bottom',
                            text=f'Trendline to goal',
                            font=dict(size=32, color="gray"),
                            arrowcolor="gray",
                            showarrow=True))

if cum_21:
    trace_name = "2021"
    fig.add_trace(
        go.Scatter(x=agg_data.index, y=agg_data["cum_21"], mode="lines", line_color=GREEN, meta=[trace_name]))
    annotations.append(dict(x="Sep", y=0.767, axref="pixel", ayref="pixel",
                            ax=-40, ay=-15,
                            xanchor='right', yanchor='bottom',
                            text=f'{trace_name}',
                            font=dict(size=32, color=GREEN),
                            arrowcolor=GREEN,
                            showarrow=True))

if cum_22:
    trace_name = "2022"
    fig.add_trace(
        go.Scatter(x=agg_data.index, y=agg_data["cum_22"], mode="lines", line_color=YELLOW, meta=[trace_name]))
    annotations.append(dict(x="Jul", y=0.463, ax=-30, ay=30,
                            xanchor='right', yanchor='top',
                            text=f' {trace_name}',
                            font=dict(size=32, color=YELLOW),
                            axref="pixel",
                            ayref="pixel",
                            arrowcolor=YELLOW,
                            showarrow=True))

if cum_23:
    trace_name = "2023"
    fig.add_trace(go.Scatter(x=agg_data.index, y=agg_data["cum_23"], mode="lines", line_color=RED, meta=[trace_name]))
    annotations.append(dict(x="Aug", y=0.572, ax=30, ay=30,
                            xanchor='left', yanchor='middle',
                            text=f' {trace_name}',
                            font=dict(size=32, color=RED),
                            axref="pixel",
                            ayref="pixel",
                            arrowcolor=RED,
                            showarrow=True))

fig.update_layout(showlegend=False, hovermode="closest", width=1100, height=600, annotations=annotations, title="",
                  margin=dict(l=50, r=50, b=50, t=50, pad=4))
fig.update_traces(hovertemplate="<b>%{x} %{meta[0]}</b><br>%{y:.3p} of goal<extra></extra>", hoverinfo="skip",
                  hoverlabel=dict(font_size=18))
fig.update_yaxes(tickformat=",.2p", range=[-0.05, 1.05], tickfont=dict(size=18), title="% of annual goal",
                 title_font_size=18)
fig.update_xaxes(tickfont=dict(size=18), range=[-0.2, 11.1])

st.plotly_chart(fig, use_container_width=False)

st.markdown("_graph is interactive, mouse over trendlines for data, click/drag to zoom in_")

percent_df = agg_data * 100
per_individual = individual_data * 100

trendline = st.column_config.NumberColumn(label="Linear", format="%.1f%%")
cy23 = st.column_config.NumberColumn(label="CY 2023", format="%.1f%%")
cy21 = st.column_config.NumberColumn(label="CY 2021", format="%.1f%%")
cy22 = st.column_config.NumberColumn(label="CY 2022", format="%.1f%%")
df_index = st.column_config.Column(label="Month")

with st.expander("Commentary on trends"):
    commentary_md = """## Commentary on trends
* 2023
    * Consistently short of monthly goals
    * As of Aug progress toward goal matches 2022
* 2022
    * Committed extra effort to sales starting in Jul to partially recover deficit
    * Still ended year ~5% behind goal
* 2021
    * Tracked closely to linear pace throughout the year
    * Finished only 2% behind goal"""

    st.markdown(commentary_md)

with st.expander("Data and description of methods"):
    description_md = ("""## Methods employed
* Collected monthly revenue numbers at the company level
    * _Information intentionally omitted for privacy_
* Divided each month's revenue by annual goal
    * "Monthly data" below
* Accumulated each month's revenue through the year
    * "Accumulated data" below
    * Shows progress toward annual goal
    * Added straight-line trend to 100% of annual goal""")
    st.markdown(description_md)
    lcol, rcol = st.columns(2)
    lcol.header("Monthly data")
    lcol.dataframe(per_individual, column_config={
        "month": df_index,
        "linear": trendline,
        "per_of_goal_21": cy21,
        "per_of_goal_22": cy22,
        "per_of_goal_23": cy23
    }, use_container_width=True)
    rcol.header("Accumulated data")
    rcol.dataframe(percent_df, column_config={
        "month": df_index,
        "linear": trendline,
        "cum_21": cy21,
        "cum_22": cy22,
        "cum_23": cy23
    }, use_container_width=True)
