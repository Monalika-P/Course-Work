from django.shortcuts import render,redirect
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django import forms

df = pd.read_csv('cleaned_subset.csv')

categorical_cols = ['Suburb','Type','Method','Regionname']
numerical_cols = ['Price','Distance','Landsize','BuildingArea','Rooms', 'Bathroom', 'Car']

def home(request):
    return render(request, "index.html")

def home_form(request):
    if request.method == 'POST':
        if 'barplot' in request.POST:
            return redirect('bar')
        elif 'scatterplot' in request.POST:
            return redirect('scatter')
    return render(request, "index.html")

def bar(request):
    # Select specific columns for display
    df_selected = df[[ 'Rooms', 'Type', 'Price', 'Method', 'Suburb','Landsize', 'BuildingArea','Regionname','Bathroom', 'Car']]

    if request.method == 'POST':

        selected_column = request.POST.get('columns')
        orientation  = request.POST.get('orientation')

        if orientation == 'Vertical':

            if selected_column in categorical_cols:

                ctype = "Categorical"

                if selected_column == 'Suburb':

                    result_df_counts = df.groupby('Suburb', as_index=False).agg({'Propertycount': 'first'})
                    result_df_counts = result_df_counts.sort_values(by='Propertycount', ascending=False)
                    result_df_counts = result_df_counts.reset_index()

                else:

                    result_df_counts = df.groupby(selected_column).size().reset_index(name='count')   

                selected_column_data = result_df_counts.to_json(orient='records')

            elif selected_column in numerical_cols:

                ctype = "Numeric"
                selected_column_data = df[selected_column].tolist()
            
            return render(request, "try.html", {'selected_column': selected_column, 'ctype': ctype, 'selected_column_data':selected_column_data, 'orientation': orientation })
        
        if orientation == 'Horizontal':
            if selected_column in categorical_cols:

                ctype = "Categorical"

                if selected_column == 'Suburb':

                    result_df_counts = df.groupby('Suburb', as_index=False).agg({'Propertycount': 'first'})
                    result_df_counts = result_df_counts.sort_values(by='Propertycount', ascending=False)
                    result_df_counts = result_df_counts.reset_index()

                else:

                    result_df_counts = df.groupby(selected_column).size().reset_index(name='count')   

                selected_column_data = result_df_counts.to_json(orient='records')

            elif selected_column in numerical_cols:

                ctype = "Numeric"
                selected_column_data = df[selected_column].tolist()
            
            return render(request, "bar_histogram.html", {'selected_column': selected_column, 'ctype': ctype, 'selected_column_data':selected_column_data, 'orientation':orientation})
        
    return render(request, "bar_histogram.html", {'df_selected': df_selected})

def scatter(request):
    return render(request, "scatter.html")

def scatterpost(request):
    if request.method == 'POST':
        selected_column = request.POST.get('scatteroptions')
        print("-"*20)
        print(selected_column)
        selected_column_data = df[selected_column].tolist()
        print(selected_column_data)
        price_data = df['Price'].tolist()
        stable_column = 'Price'
        return render(request, "scatter.html",{'selected_column': selected_column, 'selected_column_data':selected_column_data
                                               , 'price_data':price_data, 'stable_column':stable_column})
    return render(request, "scatter.html")


    
    






