import plotly.express as px
import streamlit as st


def bar_chart(
    df,
    x,
    y,
    title,
    horizontal=False
):
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        orientation="h" if horizontal else "v"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def line_chart(
    df,
    x,
    y,
    title
):
    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=title
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def histogram(
    df,
    column,
    title,
    bins=40
):
    fig = px.histogram(
        df,
        x=column,
        nbins=bins,
        title=title
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def scatter_chart(
    df,
    x,
    y,
    title
):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        opacity=0.5,
        title=title
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def box_plot(
    df,
    x,
    y,
    title
):
    fig = px.box(
        df,
        x=x,
        y=y,
        title=title
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def donut_chart(
    df,
    names,
    values,
    title
):
    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.5,
        title=title
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def heatmap(
    df,
    title
):
    fig = px.imshow(
        df,
        text_auto=".2f",
        aspect="auto",
        title=title
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )