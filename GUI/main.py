import streamlit as st
import pandas as pd
import time as t
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 50]
})

df

st.title("Pico_W_職能發展協會專案")
st.header(f"雞舍:red[溫度]和:blue[光線]狀態 :green[{t.localtime().tm_yday}]")
st.divider()

print(t.localtime())