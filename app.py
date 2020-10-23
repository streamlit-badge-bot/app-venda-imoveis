import streamlit as st

from PIL import Image
import time
import pandas as pd
import  numpy as np
import pickle
import joblib
# Html link
from bokeh.models.widgets import Div



@st.cache(allow_output_mutation=True)
def load(model_path):
    model = joblib.load(model_path)
    return model


lista_bairros = ['Moema','Itaim Bibi', 'Vila Mariana']

model_Moema = load(open('Modelo_Bairros/ExtraTreesRegressor-Moema.sav','rb'))

model_Vila_Mariana = load(open('Modelo_Bairros/ExtraTreesRegressor-Vila_Mariana.sav','rb'))

model_Itaim_Bibi = load(open('Modelo_Bairros/RandonForestRegressor-Itaim_Bibi.sav','rb'))



def main():
    """ ExtraTreesRegressor - Imoveis """
    
 
    html_page = """
    <div style="background-color:blue;padding=10px">
        <p style='color:white;text-align:center;font-size:20px;font-weight:bold'>APARTMENT</p>
    </div>
              """
    st.markdown(html_page, unsafe_allow_html=True)    

    image = Image.open("for-sale.png")
    st.sidebar.image(image,caption="",use_column_width=True)

    st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    activities = ["Home", "Search","About"]
    choice = st.sidebar.selectbox("Menu",activities)

    if choice == "Home":
        st.markdown("### Predicting the Sale Price of Apartments by Neighborhood")
        st.markdown("### Choice:")
        st.markdown("### - neighborhood and  characteristics")
        st.write(" ")
        image1 = Image.open("chaves_blue_3.png")
        st.image(image1,caption="",use_column_width=False)
    

    if choice == "Search":    

        # Escolher o bairro para o qual o regressor deve fazer as previsões
        bairro_escolhido = st.sidebar.selectbox("Neighborhood",lista_bairros)
    
    

        #st.markdown("### Selecione as caracteristicas do apartamento")
        area_total = st.slider('Total Area',min_value=50, max_value=250, value=100, step=10)
        area_util = st.slider('Useful Area',min_value=30, max_value=200, value=100, step=10)

        quarto = st.radio('Bedroom',(1 , 2, 3))
        banheiro = st.radio('Bathroom',(1,2,3))
        vaga = st.radio('Parking spaces',(1,2,3))

    
        
    
        # Choosen data
        #data = {'area_total_clean': area_total, 'area_util_clean': area_util, 'quarto_clean':quarto, 'banheiro_clean': banheiro, 'vaga_clean': vaga}

        #print(data)

        data = np.array([area_total, area_util, quarto, banheiro, vaga]).reshape(1,5)
      
      
        st.sidebar.markdown(" ") 
        #st.sidebar.markdown("#### 1- Selecione as caracteristicas")
        #st.sidebar.markdown("#### 2- Veja o valor previsto do apartamento")
        #st.sidebar.markdown(" ")

        if st.sidebar.button('Submit'):
            #bar = st.progress(0)
            #for i in range(11):
            #    bar.progress(i * 10)
            #    # wait
            #    time.sleep(0.1)

            if  bairro_escolhido == 'Moema':
                reg = model_Moema
                print("Model Moema:", model_Moema)

            if bairro_escolhido == "Vila Mariana":
               reg = model_Vila_Mariana
               print("Model Vila Mariana:", model_Vila_Mariana)

            if bairro_escolhido == "Itaim Bibi":
               reg = model_Itaim_Bibi
               print("Model Itaim Bibi:", model_Itaim_Bibi)
           

         
            result = reg.predict(data)
            result = np.expm1(result)
            result = int(result)

            print("Result:", result)
        
            pred = str(result)
            pred =  pred.replace('[','')
            pred =  pred.replace(']','')
            pred =  pred.replace('.','')

            print("Numero de casas:", len(pred))
       
            st.sidebar.markdown('## Forecast')
            if reg == model_Moema:
                st.sidebar.markdown("### Score R2: 95%")
            if reg == model_Itaim_Bibi:
                st.sidebar.markdown("### Score R2: 87%")
            if reg == model_Vila_Mariana:
               st.sidebar.markdown("### Score R2: 88%")
            
            if len(pred) == 6:
                print("6 casas")
                st.subheader("R$ "+pred[0:3]+'.'+pred[3:])

            if len (pred) == 7:
                print("7 casas")
                st.subheader("R$ "+pred[0]+'.'+pred[1:4]+'.'+pred[4:])
            
            bar = st.progress(0)
            for i in range(11):
                bar.progress(i * 10)
                # wait
                time.sleep(0.1)

    if choice == 'About':
        st.markdown("### Process:")
        st.write(" - First I did a scrap in 2k pages and gather 4k apartment sale announcements in São Paulo, Brazil")
        st.write(" - It became only 3k unique lines")
        st.write(" - Dataset had 299 neighborhoods, only neighborhoods with more than 50 announcements was used")
        st.write(" - The first neighborhood in this list was Moema with 161 ")
        st.write(" - The third was Itaim Bibi with 124 and the eighth was Vila Mariana with 77 ")
        st.write(" - The model was built using the data present in each neighborhood")
        st.markdown("### Supported by Streamlit from github")
        st.subheader("by Silvio Lima")
        
        if st.button("Linkedin"):
            js = "window.open('https://www.linkedin.com/in/silviocesarlima/')"
            html = '<img src onerror="{}">'.format(js)
            div = Div(text=html)
            st.bokeh_chart(div)      
       

    

if __name__ == '__main__':
    main()

     
