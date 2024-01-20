import streamlit as st

def main():
    st.title("Streamlit User Input Example")

    # Create a sidebar with a column for user input
    st.sidebar.header("User Input")

    # Add a text input widget in the sidebar
    user_input = st.sidebar.text_input("Enter your text:")

    # Display the user input in the main content area
    st.write("You entered:", user_input)

if __name__ == "__main__":
    main()

