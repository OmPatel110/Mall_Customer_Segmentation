import streamlit as st
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Load the pre-trained model and DataFrame
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# Define a function to plot the clusters
def plot_clusters(df, user_point=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='Annual Income (k$)', y='Spending Score (1-100)', data=df, hue='Cluster', s=70,  palette='tab10', ax=ax)
    ax.set_title('Clusters of Customers based on Annual Income and Spending Score')
    ax.set_xlabel('Annual Income (k$)')
    ax.set_ylabel('Spending Score (1-100)')
    ax.grid(True)
    
    # Highlight the user point if provided
    if user_point:
        ax.scatter(user_point[0], user_point[1], color='black', marker='o', s=80, label='Predicted Customer')
        ax.legend()

    # Show the plot
    st.pyplot(fig)

def main():
    # Custom CSS for styling the title
    title_style = """
    <style>
        /* Custom CSS for the title */
        .title-text {
            color: #0874D1; /* Change text color to blue */
            font-size: 36px; /* Increase font size */
            font-weight: bold; /* Make text bold */
            text-align: left; /* Center-align text */
            margin-bottom: 20px; /* Add some bottom margin */
            margin-top: 0px;
        }
    </style>
    """
    # Display the styled title with emoji
    st.markdown(title_style, unsafe_allow_html=True)
    st.markdown("<h1 class='title-text'>🔍 Revealing Shopping Personalities: Customer Segmentation 🛍️</h1>", unsafe_allow_html=True)

    # Set input field width
    st.markdown(
    """
    <style>
    /* Input field width */
        div.stTextInput > div:first-child input[type="text"],
        div.stNumberInput > div:first-child input[type="number"],
        div.stSelectbox > div:first-child select {
        width: 300px;
        height: 40px;
        border-radius: 8px;
        border: 2px solid #1E88E5;
        padding: 5px 10px;
        font-size: 24px;
        color: #1E88E5;
        background-color: #F5F5F5;
        }

    /* Increase spacing between input fields */
        .stTextInput, .stNumberInput, .stSelectbox {
        margin-bottom: 20px;
        }

    /* Style the select box */
        div.stSelectbox > div:first-child::after {
        color: #1E88E5;
        }
    </style>
    """, unsafe_allow_html=True)

    # Display the input field for annual income
    annual_income = st.number_input('Annual Income (in k$)', min_value=10, max_value=200, value=10, step=1)

    # Spending Score
    spending_score = st.number_input('Spending Score (1-lowest, 100-highest)', min_value=1, max_value=100, value=1, step=1)

    # Initialize user point
    user_point = None

    # Display Prediction
    if st.button('Predict'):
        # Convert user input to a list
        user_point = [annual_income, spending_score]
    
        # Predict the cluster for the user point and display the prediction
        predicted_cluster = pipe.predict([user_point])
        cluster_map = {
            0: ["Cluster 0: Mid Income, Mid Spending", "This cluster represents customers with moderate income and moderate spending habits. They are neither high spenders nor low spenders"],
            1: ["Cluster 1: High Income, Low Spending","Customers in this cluster have high income but exhibit conservative spending behavior. They may prioritize savings or investments over unnecessary spending."],
            2: ["Cluster 2: Low Income, Low Spending","This cluster consists of customers with low income and minimal spending. They may prioritize essential purchases and have limited capacity for additional spending."],
            3: ["Cluster 3: Low Income, High Spending","Customers in this cluster have low income but exhibit high spending. They may engage in impulse buying or prioritize lifestyle purchases despite financial constraints."],
            4: ["Cluster 4: High Income, High Spending","This cluster comprises customers with high income and excessive spending habits. They have significant purchasing power and may indulge in luxury goods or premium experiences."]
        }
        prediction_lines = cluster_map.get(predicted_cluster[0], [" "])
        for line in prediction_lines:
            st.write(line)

    # Create an expander for displaying the cluster plot
    with st.expander("Visualize Clusters", expanded=False):
        # Call the function to plot the clusters with the user point highlighted
        plot_clusters(df, user_point)

if __name__ == "__main__":
    main()
