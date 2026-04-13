# Import python packages.
import streamlit as st

# Write directly to the app.
st.title(f"Example Streamlit App :balloon: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

st.markdown("""
- :page_with_curl: [Streamlit open source documentation](https://docs.streamlit.io)
- :snowflake: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- :snowboarder: [Snowpark Session documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/session)
- :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)
- :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)
""")

# Create a database connection to Snowflake.
conn = st.connection("snowflake")

# Create a Snowpark session from the connection.
# This provides a few helpers on top of a standard Python connection.
# If you want to use a plain Snowflake connection instead, you can create
# one with conn.cursor().
session = conn.session()
my_dataframe = session.table("smoothies.public.fruit_options")
#st.dataframe(data=my_dataframe, use_container_width=True)


name=st.text_input('Name on Smoothie')
st.write('Name on Smoothie :'+name)
options = st.multiselect(
    "What are your favorite Fruits?",
    ["Apples", "Blueberries", "Dragon Fruit", "Elderberries","Fig"],max_selections=4
)
ingredients_string=''
if options:  
   st.write("You selected:", options)
   st.text(options)
   
   for each_fruit in options: 
       ingredients_string += each_fruit+' ' 
   st.write(ingredients_string) 

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
                    values ('""" + ingredients_string + """','""" + name + """')"""

#st.write(my_insert_stmt) 

time_to_insert=st.button("Submit to order")

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!'+name+'!', icon="✅")
    st.stop() 
#st.write("You selected:", options)
