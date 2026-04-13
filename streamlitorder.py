# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col,when_matched
# Write directly to the app.
st.title(f"Example Streamlit App :balloon: {st.__version__}")


# Create a database connection to Snowflake.
conn = st.connection("snowflake")

# Create a Snowpark session from the connection.
# This provides a few helpers on top of a standard Python connection.
# If you want to use a plain Snowflake connection instead, you can create
# one with conn.cursor().
session = conn.session()

my_dataframe = session.table("smoothies.public.orders") \
    .filter(col("ORDER_FILLED") == 0) \
    .collect()
if my_dataframe:
#st.dataframe(data=my_dataframe, use_container_width=True)
    editable_dataframe=st.data_editor(my_dataframe)
   
    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_dataframe)
    og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
    time_to_insert=st.button("Submit")
    if time_to_insert:
       st.success("Some one clicked the button", icon= '👍') 
else:
    st.success("No pending orders", icon= '👍') 
