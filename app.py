from flask import  Flask, render_template, request, jsonify,session
import pymysql.cursors
import pandas as pd

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)



################################ STATE WISE HEATMAP CORRELATION ######################################
def durex_state_save_heatmap_and_correlation(excel_file_path, save_path):
       df1 = pd.read_excel(excel_file_path)
       df2 = df1.copy()
       df2 = df2.iloc[:-1,:]
       filtered_CONDOMS = df2[df2['PRODUCT'] == 'RECKITT BENCKISER']
       filtered_CONDOMS = filtered_CONDOMS.reset_index(drop=True)
       filtered_CONDOMS.set_index('MARKET', inplace=True)
       filtered_CONDOMS.index.name = None
       transposed_filtered_CONDOMS = filtered_CONDOMS.T
       start_date = 'JUN20'
       end_date = 'MAY23'
       transposed_filtered_CONDOMS = transposed_filtered_CONDOMS.loc[start_date:end_date]
       state = ['Punjab', 'HP-JK', 'Haryana', 'Rajasthan', 'Uttar Pradesh',
       'Uttaranchal', 'Assam', 'North East', 'Bihar', 'Jharkhand', 'Orissa',
       'West Bengal', 'Gujarat', 'Madhya Pradesh', 'Chhattisgarh',
       'Maharashtra', 'Andhra Pradesh', 'Telangana', 'Kerala', 'Tamil Nadu', 'Karnataka']

       transposed_filtered_CONDOMS = transposed_filtered_CONDOMS[state]
       transposed_filtered_CONDOMS = transposed_filtered_CONDOMS.reset_index()
       transposed_filtered_CONDOMS2 = transposed_filtered_CONDOMS.iloc[:,1:]
       transposed_filtered_CONDOMS.set_index('index', inplace=True)
       transposed_filtered_CONDOMS = transposed_filtered_CONDOMS.apply(pd.to_numeric, errors='coerce')
       corr_matrix = transposed_filtered_CONDOMS.corr()
       plt.figure(figsize=(14, 10))
       sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
       plt.title('Pearson Correlation Heatmap of State wise Durex Sales Data')
       plt.xlabel('State')
       plt.ylabel('State')

       # # Save the heatmap as an image file (e.g., PNG)
       heatmap_image_path = save_path + '_durex_state_heatmap.png'
       plt.savefig(heatmap_image_path)

       # Save the heatmap data (DTW distances) to a CSV file
       correlation_data_path  = save_path + '_durex_state_correlation_data.csv'
       corr_matrix.to_csv(correlation_data_path )

       np.fill_diagonal(corr_matrix.values, -2)

       # Get the top 5 correlated city pairs (excluding diagonal and same city pairs)
       correlations = corr_matrix.stack().sort_values(ascending=False)
       top_corr_pairs = []

       for (city1, city2), correlation in correlations.iteritems():
           if city1 != city2 and (city2, city1) not in top_corr_pairs:
               top_corr_pairs.append((city1, city2))
               if len(top_corr_pairs) >= 5:
                   break
       
       TOP_CORR=[]
       # Print the top correlated city pairs and their correlation values
       for city1, city2 in top_corr_pairs:
           correlation = corr_matrix.loc[city1, city2]
           print(f"{city1} - {city2}: {correlation}")
           TOP_CORR.append((city1,city2,correlation))

       df_top=pd.DataFrame(TOP_CORR,columns=['State1','State2','Correlation%'])

       return heatmap_image_path,correlation_data_path,df_top


########################## CITY WISE HEATMAP CORRELATION #########################

def durex_cities_save_heatmap_and_correlation(excel_file_path, save_path):
       df1 = pd.read_excel(excel_file_path)
       df2 = df1.copy()
       df2 = df2.iloc[:-1,:]
       filtered_CONDOMS = df2[df2['PRODUCT'] == 'RECKITT BENCKISER']
       filtered_CONDOMS = filtered_CONDOMS.reset_index(drop=True)
       filtered_CONDOMS.set_index('MARKET', inplace=True)
       filtered_CONDOMS.index.name = None
       transposed_filtered_CONDOMS = filtered_CONDOMS.T
       start_date = 'JUN20'
       end_date = 'MAY23'
       transposed_filtered_CONDOMS = transposed_filtered_CONDOMS.loc[start_date:end_date]
       cities = ['Ahmedabad', 'Bangalore', 'Chennai', 'Hyderabad', 'Kolkata', 'Mumbai','Pune', 'Delhi']
       transposed_filtered_CONDOMS = transposed_filtered_CONDOMS[cities]
       transposed_filtered_CONDOMS = transposed_filtered_CONDOMS.reset_index()
       transposed_filtered_CONDOMS2 = transposed_filtered_CONDOMS.iloc[:,1:]
       transposed_filtered_CONDOMS.set_index('index', inplace=True)
       transposed_filtered_CONDOMS = transposed_filtered_CONDOMS.apply(pd.to_numeric, errors='coerce')
       corr_matrix = transposed_filtered_CONDOMS.corr()
       plt.figure(figsize=(12, 8))
       sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
       plt.title('Pearson Correlation Heatmap of Cities wise Durex Sales Data')
       plt.xlabel('Cities')
       plt.ylabel('Cities')
      
       # # Save the heatmap as an image file (e.g., PNG)
       heatmap_image_path = save_path + '_durex_cities_heatmap.png'
       plt.savefig(heatmap_image_path)

       # Save the heatmap data (DTW distances) to a CSV file
       correlation_data_path  = save_path + '_durex_cities_correlation_data.csv'
       corr_matrix.to_csv(correlation_data_path )

       np.fill_diagonal(corr_matrix.values, -2)

       # Get the top 5 correlated city pairs (excluding diagonal and same city pairs)
       correlations = corr_matrix.stack().sort_values(ascending=False)
       top_corr_pairs = []

       for (city1, city2), correlation in correlations.iteritems():
           if city1 != city2 and (city2, city1) not in top_corr_pairs:
               top_corr_pairs.append((city1, city2))
               if len(top_corr_pairs) >= 5:
                   break
       
       TOP_CORR=[]
       # Print the top correlated city pairs and their correlation values
       for city1, city2 in top_corr_pairs:
           correlation = corr_matrix.loc[city1, city2]
           print(f"{city1} - {city2}: {correlation}")
           TOP_CORR.append((city1,city2,correlation))

       df_top=pd.DataFrame(TOP_CORR,columns=['City1','City2','Correlation%'])

       return heatmap_image_path,correlation_data_path,df_top



def format_age(corr):
    if corr < 25:
        return f'<span style="color: red;" class="age-less-than-25">{corr}</span>'
    elif corr == 25:
        return f'<span style="color: red;" class="age-equal-to-25">{corr}</span>'
    else:
        return corr


#{'id': 1, 'username': 'MITM_RECKITT', 'password': '1234'}

app = Flask(__name__)
@app.route('/')

def sun():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def contact():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Handle the form submission data here
        name = request.form['username']
        password = request.form['password']
        # cursors.execute('select * from login_credentials  WHERE username = % s AND password = % s', (name, password, ))
        # re=cursors.fetchone()

        if name=='MITM_RECKITT' and password=='1234':
            return render_template('index.html')
        else:
            msg = "<script>alert('Incorrect Credentials!');</script>"
            return render_template('login.html',msg=msg)

@app.route('/index', methods=['POST'])
def index1():
    if request.method == 'POST':
        ######### BRAND ############
        search_filter = request.form['option1']
        ######### STATE ###########
        selected_option = request.form['option']  

        brand=str(search_filter).lower()
        print(search_filter)
        print(selected_option)

        if selected_option=='State':
            excel_file_path = "static\\State\\val_2023.xlsx"
            save_path = 'static\\State\\'
            region = selected_option

            heatmap_image_path,correlation_data_path,df_top=durex_state_save_heatmap_and_correlation(excel_file_path, save_path)

            df_top['Correlation%'] = df_top['Correlation%'].apply(lambda x: format_age(x))
            brand=str(search_filter).lower()
            image_path='static\\State\\_'+str(brand)+'_state_heatmap.png'
            Excel_sheet='static\\State\\_'+str(brand)+'_state_correlation_data.csv'
            Image_url=image_path

            print("img:::",image_path)

            table_html = df_top.to_html(classes='table table-bordered table-hover', index=False, escape=False)

            return render_template('output.html', table_html=table_html,image_path=image_path,search_filter=search_filter,Excel_sheet=Excel_sheet,excel_file_path=excel_file_path,Image_url=Image_url,region=region)

        elif selected_option=='City':
            excel_file_path = "static\\City\\val_2023.xlsx"
            save_path = 'static\\City\\'
            region=selected_option
            heatmap_image_path,correlation_data_path,df_top=durex_cities_save_heatmap_and_correlation(excel_file_path, save_path)


            df_top['Correlation%'] = df_top['Correlation%'].apply(lambda x: format_age(x))
            brand = str(search_filter).lower()
            image_path='static\\City\\_'+str(brand)+'_cities_heatmap.png'
            Excel_sheet='static\\City\\_'+str(brand)+'_cities_correlation_data.csv'
            Image_url=image_path
            print("img:::",image_path)

            table_html = df_top.to_html(classes='table table-bordered table-hover', index=False, escape=False)

            return render_template('output.html', table_html=table_html,image_path=image_path,search_filter=search_filter,Excel_sheet=Excel_sheet,excel_file_path=excel_file_path,Image_url=Image_url,region=region)

        # else:
        #     print('error not selected correctly')

if __name__ == '__main__':
    app.run(debug=True)

