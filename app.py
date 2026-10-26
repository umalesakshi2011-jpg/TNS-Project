### Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import StratifiedKFold, cross_val_score


from sklearn.model_selection import GridSearchCV, RandomizedSearchCV


import joblib
import streamlit as st

df = pd.read_csv(r"D:\Machine Leraning\TNS\capstone_project\manufacturing_data.csv")
# print(df.sample(5))
# print(f"shape of dataset {df.shape}")
# print(df.info())
# print(df.describe())
df['Parts_Per_Hour'] = pd.to_numeric(
    df['Parts_Per_Hour'].astype(str).str.replace('+', '', regex=False),
    errors='coerce'
)
df = df.dropna(subset=['Parts_Per_Hour']).copy()
TARGET = 'Parts_Per_Hour'
NUMERIC_FEATURES = [
    'Injection_Temperature', 'Injection_Pressure', 'Cycle_Time',
    'Cooling_Time', 'Material_Viscosity', 'Ambient_Temperature',
    'Machine_Age', 'Operator_Experience', 'Maintenance_Hours',
    'Efficiency_Score', 'Machine_Utilization'
]
CATEGORICAL_FEATURES = ['Shift', 'Machine_Type', 'Material_Grade', 'Day_of_Week']

X = df.drop(columns=[TARGET, 'Timestamp', 'Total_Cycle_Time', 'Temperature_Pressure_Ratio'])
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)
# print('Training rows:', len(X_train))
# print('Testing rows:', len(X_test))

numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, NUMERIC_FEATURES),
    ('cat', categorical_pipeline, CATEGORICAL_FEATURES)
])

linear_model = Pipeline([
    ('prep', preprocessor),
    ('model', LinearRegression())
])

linear_model.fit(X_train, y_train)

y_train_pred = linear_model.predict(X_train)
y_test_pred = linear_model.predict(X_test)
mae_train = mean_absolute_error(y_train,y_train_pred)
mse_train = mean_squared_error(y_train,y_train_pred)
r2_train = r2_score(y_train, y_train_pred)

#testing data evaluation
mae_test = mean_absolute_error(y_test,y_test_pred)
mse_test = mean_squared_error(y_test,y_test_pred)
r2_test = r2_score(y_test,y_test_pred)


# print("Training: ")
# print(f"MAE : {mae_train}")
# print(f"MSE : {mse_train}")
# print(f"R2 : {r2_train}")

# print("Testing :")
# print(f"MAE : {mae_test}")
# print(f"MSE : {mse_test}")
# print(f"R2 : {r2_test}")
joblib.dump(linear_model,"capstone_project.joblib")

model = joblib.load("capstone_project.joblib")


st.set_page_config(
    page_title="Manufacturing Output Prediction",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Manufacturing Equipment Output Prediction")
st.write("Predict the hourly production output of an injection molding machine ")

st.divider()
st.subheader("⚙️ Machine Parameters")

col1, col2 = st.columns(2)

with col1:
    Injection_Temperature = st.number_input("Injection Temperature" )  
    Injection_Pressure = st.number_input( "Injection Pressure" )
    Cycle_Time = st.number_input("Cycle Time" )

with col2:
   Cooling_Time = st.number_input( "Cooling Time" )
   Machine_Utilization = st.number_input( "Machine Utilization" )
   Efficiency_Score= st.number_input( "Efficiency Score")

st.subheader("👷 Operator & Maintenance")
col1, col2 = st.columns(2)
with col1:
    Operator_Experience = st.number_input( "Operator Experience" )

with col2:
    Maintenance_Hours = st.number_input("Maintenance Hours" )

st.subheader("🧪 Material Information")

col1, col2 = st.columns(2)

with col1:
   Material_Viscosity = st.number_input( "Material Viscosity" )
with col2:
    Material_Grade = st.selectbox("Material Grade", ["Economy", "Standard", "Premium"])


st.subheader("🌡️ Environmental Information")

col1, col2 = st.columns(2)

with col1:
    Ambient_Temperature = st.number_input("Ambient Temperature")

with col2:
    Day_of_Week = st.selectbox(
        "Day of Week",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
    )

st.subheader("🏭 Machine & Shift Information")

col1, col2 = st.columns(2)

with col1:
    Machine_Type = st.selectbox( "Machine Type",["Type_A", "Type_B","Type_C"] )
    Machine_Age = st.number_input("Machine Age")

with col2:
    Shift = st.selectbox( "Shift",  ["Day", "Night", "Evening"]  ) 



input_row =pd.DataFrame( [{
    "Injection_Temperature":Injection_Temperature,
    "Injection_Pressure":Injection_Pressure,
    "Cycle_Time":Cycle_Time,
    "Cooling_Time":Cooling_Time,
    "Material_Viscosity":Material_Viscosity,
    "Machine_Age":Machine_Age,
    "Ambient_Temperature":Ambient_Temperature,
    "Operator_Experience":Operator_Experience,
    "Maintenance_Hours":Maintenance_Hours,
    "Efficiency_Score":Efficiency_Score,
    "Machine_Utilization":Machine_Utilization,
    "Shift":Shift,
    "Machine_Type":Machine_Type,
    "Material_Grade":Material_Grade,
    "Day_of_Week":Day_of_Week  
}])
prediction = linear_model.predict(input_row)[0]

st.divider()
if st.button("🔮 Predict Parts Per Hour", use_container_width=True):
    st.success(f"Parts per hour : {prediction :.2f}")

    