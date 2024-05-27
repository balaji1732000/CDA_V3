import streamlit as st
import pandas as pd
import os
from utils import developer_info_static
from plots import (
    list_all,
    distribution_histogram,
    distribution_boxplot,
    count_Y,
    box_plot,
    violin_plot,
    strip_plot,
    density_plot,
    multi_plot_heatmap,
    multi_plot_scatter,
    multi_plot_line,
    word_cloud_plot,
    world_map,
    scatter_3d,
)


# # Define the directory where processed files are saved
# processed_files_dir = "F:\Documents backup\AI Projects\CDA_V2\CDA_V2\temp\incidents.csv"
st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .css-18e3th9 {padding: 0 1rem;}
    .css-1lcbmhc, .css-1d391kg {padding: 0 1rem; max-width: 100% !important;}
    .main .block-container {padding: 0 1rem; max-width: 100%;}

    /* Change the background color */
    body {
        background-color: #f0f8ff; /* AliceBlue background color */
    }
    .main .block-container {
        background-color: #ffffff; /* White background for the container */
        border-radius: 10px;
        padding: 2rem;
    }

    .stTabs [data-baseweb="tab"]:hover {
       background-color: #f0f0f0; 
       color: #000; 
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"]{
        background-color: #fff; 
        color: #000; 
        border-bottom: 2px solid #ff4b4b;
    }
    .css-1d391kg {font-family: 'Arial', sans-serif; font-size: 1rem;}

    /* Change the button colors */
    .stButton>button {
        background-color: #304666; /* Button background color (Green) */
        color: #fff; /* Button text color */
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #fffff; /* Button hover color */
    }

    /* Change the select box styles */
    .stSelectbox>div>div>div {
        padding: 0.5rem;
        background-color: #fff; /* Light cyan background color for select box */
    }
    .css-1hb8ztp {
        font-size: 1rem;
        color: #333;
    }
    .css-10trblm {
        padding: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Helper function to get command-line arguments
def get_command_line_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataVizFile", type=str, required=True, help="Path to the data file"
    )
    args = parser.parse_args()
    return args


def display_word_cloud(text):
    _, word_cloud_col, _ = st.columns([1, 3, 1])
    with word_cloud_col:
        word_fig = word_cloud_plot(text)
        if word_fig == -1:
            st.error("Data not supported")
        else:
            st.pyplot(word_cloud_plot(text))


def data_visualization(DF):
    st.divider()
    st.subheader("Data Visualization")
    attributes = DF.columns.tolist()
    # Three tabs for three kinds of visualization
    single_tab, multiple_tab, advanced_tab = st.tabs(
        [
            "Single Data Visualization",
            "Combined Data Visualization",
            "Advanced Visualization",
        ]
    )

    # Single attribute visualization
    with single_tab:
        _, col_mid, _ = st.columns([1, 5, 1])
        with col_mid:
            plot_area = st.empty()
        col1, col2 = st.columns(2)
        with col1:
            att = st.selectbox(
                label="Select an attribute to visualize:",
                options=attributes,
                index=len(attributes) - 1,
            )
            st.write(f"Attribute selected: :green[{att}]")
        with col2:
            plot_types = [
                "Donut chart",
                "Violin plot",
                "Distribution histogram",
                "Boxplot",
                "Density plot",
                "Strip plot",
                "Distribution boxplot",
            ]
            plot_type = st.selectbox(
                key="plot_type1",
                label="Select a plot type:",
                options=plot_types,
                index=0,
            )
            st.write(f"Plot type selected: :green[{plot_type}]")
        if plot_type == "Distribution histogram":
            fig = distribution_histogram(DF, att)
            plot_area.pyplot(fig)
        elif plot_type == "Distribution boxplot":
            fig = distribution_boxplot(DF, att)
            if fig == -1:
                plot_area.error("The attribute is not numeric")
            else:
                plot_area.pyplot(fig)
        elif plot_type == "Donut chart":
            fig = count_Y(DF, att)
            plot_area.plotly_chart(fig)
        elif plot_type == "Boxplot":
            fig = box_plot(DF, [att])
            plot_area.plotly_chart(fig)
        elif plot_type == "Violin plot":
            fig = violin_plot(DF, [att])
            plot_area.plotly_chart(fig)
        elif plot_type == "Strip plot":
            fig = strip_plot(DF, [att])
            plot_area.plotly_chart(fig)
        elif plot_type == "Density plot":
            fig = density_plot(DF, att)
            plot_area.plotly_chart(fig)
    # Multiple attribute visualization
    with multiple_tab:
        col1, col2 = st.columns([6, 4])
        with col1:
            options = st.multiselect(
                label="Select multiple attributes to visualize:",
                options=attributes,
                default=[],
            )
        with col2:
            plot_types = [
                "Violin plot",
                "Boxplot",
                "Heatmap",
                "Strip plot",
                "Line plot",
                "Scatter plot",
            ]
            plot_type = st.selectbox(
                key="plot_type2",
                label="Select a plot type:",
                options=plot_types,
                index=0,
            )
        _, col_mid, _ = st.columns([1, 5, 1])
        with col_mid:
            plot_area = st.empty()
        if options:
            if plot_type == "Scatter plot":
                fig = multi_plot_scatter(DF, options)
                if fig == -1:
                    plot_area.error("Scatter plot requires two attributes")
                else:
                    plot_area.pyplot(fig)
            elif plot_type == "Heatmap":
                fig = multi_plot_heatmap(DF, options)
                if fig == -1:
                    plot_area.error("The attributes are not numeric")
                else:
                    plot_area.pyplot(fig)
            elif plot_type == "Boxplot":
                fig = box_plot(DF, options)
                if fig == -1:
                    plot_area.error("The attributes are not numeric")
                else:
                    plot_area.plotly_chart(fig)
            elif plot_type == "Violin plot":
                fig = violin_plot(DF, options)
                if fig == -1:
                    plot_area.error("The attributes are not numeric")
                else:
                    plot_area.plotly_chart(fig)
            elif plot_type == "Strip plot":
                fig = strip_plot(DF, options)
                if fig == -1:
                    plot_area.error("The attributes are not numeric")
                else:
                    plot_area.plotly_chart(fig)
            elif plot_type == "Line plot":
                fig = multi_plot_line(DF, options)
                if fig == -1:
                    plot_area.error("The attributes are not numeric")
                elif fig == -2:
                    plot_area.error("Line plot requires two attributes")
                else:
                    plot_area.pyplot(fig)
    # Advanced visualization
    with advanced_tab:
        st.subheader("3D Scatter Plot")
        column_1, column_2, column_3 = st.columns(3)
        with column_1:
            x = st.selectbox(
                key="x", label="Select the x attribute:", options=attributes, index=0
            )
        with column_2:
            y = st.selectbox(
                key="y",
                label="Select the y attribute:",
                options=attributes,
                index=1 if len(attributes) > 1 else 0,
            )
        with column_3:
            z = st.selectbox(
                key="z",
                label="Select the z attribute:",
                options=attributes,
                index=2 if len(attributes) > 2 else 0,
            )
        if st.button("Generate 3D Plot"):
            _, fig_3d_col, _ = st.columns([1, 3, 1])
            with fig_3d_col:
                fig_3d_1 = scatter_3d(DF, x, y, z)
                if fig_3d_1 == -1:
                    st.error("Data not supported")
                else:
                    st.plotly_chart(fig_3d_1)
        st.divider()
        st.subheader("World Cloud")
        upload_txt_checkbox = st.checkbox("Upload a new text file instead")
        if upload_txt_checkbox:
            uploaded_txt = st.file_uploader(
                "Choose a text file", accept_multiple_files=False, type="txt"
            )
            if uploaded_txt:
                text = uploaded_txt.read().decode("utf-8")
                display_word_cloud(text)
        else:
            text_attr = st.selectbox(
                label="Select the text attribute:", options=attributes, index=0
            )
            if st.button("Generate Word Cloud"):
                text = DF[text_attr].astype(str).str.cat(sep=" ")
                display_word_cloud(text)
        st.divider()
        st.subheader("World Heat Map")
        col_1, col_2 = st.columns(2)
        with col_1:
            country_col = st.selectbox(
                key="country_col",
                label="Select the country attribute:",
                options=attributes,
                index=0,
            )
        with col_2:
            heat_attribute = st.selectbox(
                key="heat_attribute",
                label="Select the attribute to display in heat map:",
                options=attributes,
                index=len(attributes) - 1,
            )
        if st.button("Show Heatmap"):
            _, map_col, _ = st.columns([1, 3, 1])
            with map_col:
                world_fig = world_map(DF, country_col, heat_attribute)
                if world_fig == -1:
                    st.error("Data not supported")
                else:
                    st.plotly_chart(world_fig)
    st.divider()
    # Data Overview
    st.subheader("Data Overview")
    if "data_origin" not in st.session_state:
        st.session_state.data_origin = DF
    st.dataframe(st.session_state.data_origin.describe(), width=1200)
    if "overall_plot" not in st.session_state:
        st.session_state.overall_plot = list_all(st.session_state.data_origin)
    st.pyplot(st.session_state.overall_plot)
    st.divider()
    developer_info_static()


# Read the latest processed file
# def get_latest_processed_file():
#     files = os.listdir(processed_files_dir)
#     if not files:
#         st.error("No processed files found.")
#         return None
#     latest_file = max(
#         files, key=lambda x: os.path.getctime(os.path.join(processed_files_dir, x))
#     )
#     file_path = os.path.join(processed_files_dir, latest_file)
#     return file_path


# Main function to load the data and call the visualization function
def main():

    args = get_command_line_args()
    dataVizFile = args.dataVizFile

    # st.write(f"Received file path: {dataVizFile}")  # Debugging statement

    if not dataVizFile:
        st.error("No data file provided.")
        return

    if not os.path.exists(dataVizFile):
        st.error(f"File does not exist: {dataVizFile}")
        return

    file_extension = os.path.splitext(dataVizFile)[-1].lower()
    # st.write(f"File extension: {file_extension}")  # Debugging statement

    try:
        if file_extension == ".csv":
            df = pd.read_csv(dataVizFile)
        elif file_extension == ".xlsx":
            df = pd.read_excel(dataVizFile)
        else:
            st.error("Unsupported file format")
            return
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return

    # st.write("File loaded successfully!")  # Debugging statement
    data_visualization(df)


if __name__ == "__main__":
    main()
