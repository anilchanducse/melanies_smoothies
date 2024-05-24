# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your Smoothie will be:', name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingrediants_list=st.multiselect(
    'Choose upto 5 ingrediants:'
    ,my_dataframe
    ,max_selections=5
    )
if ingrediants_list:
    
    ingrediants_string=''
    
    for x in ingrediants_list:
        ingrediants_string += x+' '
        st.subheader(x + ' Nutrition Information')        
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +x)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    st.write(ingrediants_string) 

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingrediants_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button("Submit Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered,'+ name_on_order+'!', icon="✅")



