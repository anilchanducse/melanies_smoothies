# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingrediants_list=st.multiselect(
    'Choose upto 5 ingrediants:'
    ,my_dataframe
    )
if ingrediants_list:
    
    ingrediants_string=''
    
    for x in ingrediants_list:
        ingrediants_string += x+' '

    st.write(ingrediants_string) 

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingrediants_string + """')"""

    #st.write(my_insert_stmt)
    time_to_insert=st.button("Submit Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")
