# Conversion of BaselineController_Main to python
# Author: Christopher Crouch

#import necessary functions
import numpy as np
import pandas as pd
import os

def BaselineController_Main():
    
    #----------------------------- OS Information ----------------------------%
    
    OS = 2 # 1 - Linux ; 2 - Windows-Laptop ; 3 - Windows-PC
    
    #-------------------------- Simulation Step Sizes ------------------------%
    
    FileRes=10                         # in Minutes
    Simulation_StepSize = FileRes/60   # in Hours
    StepSize = FileRes*60              # in Seconds
    SmartCommunity_ControllerType=1    # 1 = Smart Local Controller ; 2 = Dumb Local Controller
    
    #-------------------------- Simulation Parameters ------------------------%

    SimulationType = 0 # Important for Single Large House Simulation [1,2,3,4,5,6,7,8] == [N_PV_Bat_EV, N_PV_Bat, N_PV_EV, N_Bat_EV, N_PV, N_Bat, N_EV, N_None]
    LoadDataType=2 # 1 - File Generated from Preprocessed Pecan Street Data files ; 2 - .mat File already exists
    WeatherDataType=2 # 1 - File Generated from Preprocessed NSRDB File ; 2 - .mat File already exists
    Single_House_Plotting_Index=1 # House Index for Single House Plotting
    
    #------------------------- Community Specification -----------------------%

    N_PV_Bat=1     # Houses with both PV and Battery
    N_PV=1         # Houses with just PV
    N_Bat=1        # Houses with just Battery
    N_None=1       # Houses with niether PV and Battery
    
    # Computing Total Number of Houses
    N_House=N_PV_Bat+N_PV+N_Bat+N_None
    N_House_Vector=[N_PV_Bat,N_Bat,N_PV,N_None]
    
    #----------------- Plant Initial Condition Specification -----------------%

    # House Temperature Intial Condition
    T_AC_Base=24
    T_House_Variance=0.5
    
    # Battery Initial Condition
    N1=1;                          # User Input - Battery Max Changing Factor
    Battery_Energy_Max = 13.5*N1

    #--------------------- Simulation Period Specification -------------------%

    # Load Computation Start Date
    StartYear=2017     # User Defined
    StartMonth=9      # User Defined
    StartDay=11         # User Defined
    StartTime=0        # User Defined
    
    # Load Computation End Date
    EndYear=2017       # User Defined
    EndMonth=9        # User Defined
    EndDay=18          # User Defined
    EndTime=24-(FileRes/60)          #24-(FileRes/60)
    
    #----------------------- Folder Paths Specification ----------------------%

    ImageFolder_Name='Gainesville_BaseLine_7DayTest_SC_PVBat1_Bat1_PV1_None1_SCL1_'
    SimulationData_FileName='FigurePlotterData_Gainesville_BaseLine_7DayTest_SC_PVBat1_Bat1_PV1_None1_SLC1'
    SimulationPerformanceData_FileName='PerformanceData_Gainesville_BaseLine_7DayTest_SC_PVBat1_Bat1_PV1_None1_SLC1'
    LoadData_FileName='PecanStreet_LoadData_SC_PVBat1_Bat1_PV1_None1'
    WeatherData_FileName='Gainesville_Irma'
    
    #-------------------- Weather Data Location and Period -------------------%

    # Getting to Weather Data Folder in the Correct OS Folder
    if OS == 1: #Linux
        WeatherDataFile_Path="/home/ninadgaikwad/Dropbox (UFL)/NinadGaikwad_PhD/Gaikwad_Research/Gaikwad_Research_Work/19_Resiliency/codes/Matlab_Scripts_New/CCTA_2020/Laptop_Final_Improved/DwellTime_CNCL_WithoutL1/Data/Gainesville_2017_To_2017_WeatherData_NSRDB_30minTo10minRes.csv"
        LoadDataFolder_Path="/home/ninadgaikwad/Dropbox (UFL)/NinadGaikwad_PhD/Gaikwad_Research/Gaikwad_Research_Work/20_Gaikwad_SmartCommunity/data/PreProcessedFiles/10minute_data_austin_HouseWise/"
    elif OS == 2:  #Windows-Laptop
         WeatherDataFile_Path = r"C:\Users\ninad\Dropbox (UFL)\NinadGaikwad_PhD\Gaikwad_Research\Gaikwad_Research_Work\19_Resiliency\codes\Matlab_Scripts_New\CCTA_2020\Laptop_Final_Improved\DwellTime_CNCL_WithoutL1\Data\Gainesville_2017_To_2017_WeatherData_NSRDB_30minTo10minRes.csv"
         LoadDataFolder_Path= 'C:\\Users\\ninad\\Dropbox (UFL)\\NinadGaikwad_PhD\\Gaikwad_Research\\Gaikwad_Research_Work\\20_Gaikwad_SmartCommunity\\data\\PreProcessedFiles\\10minute_data_austin_HouseWise\\'
    elif OS == 3: # Windows-PC  
         WeatherDataFile_Path = "C:\\Users\\Me!\\Dropbox (UFL)\\NinadGaikwad_PhD\\Gaikwad_Research\\Gaikwad_Research_Work\\19_Resiliency\\codes\\Matlab_Scripts_New\\CCTA_2020\\Laptop_Final_Improved\\DwellTime_CNCL_WithoutL1\\Data\\Gainesville_2017_To_2017_WeatherData_NSRDB_30minTo10minRes.csv"
         LoadDataFolder_Path = "C:\\Users\\Me!\\Dropbox (UFL)\\NinadGaikwad_PhD\\Gaikwad_Research\\Gaikwad_Research_Work\\20_Gaikwad_SmartCommunity\\data\\PreProcessedFiles\\10minute_data_austin_HouseWise\\"

    # Weather Data Extraction
    # Creating Simulation_Params Struct (Dict data structure used in python)
    Simulation_Params = {}
    Simulation_Params[FileRes] = FileRes
    Simulation_Params[Simulation_StepSize] = Simulation_StepSize
    Simulation_Params[StepSize] = StepSize
    Simulation_Params[SmartCommunity_ControllerType] = SmartCommunity_ControllerType
    
    # Creating HEMSWeatherData_Input Struct (Dict data structure used in python)

    HEMSWeatherData_Input={}; # Empty dict
    HEMSWeatherData_Input[WeatherDataFile_Path]=WeatherDataFile_Path;
    HEMSWeatherData_Input[StartYear]=StartYear
    HEMSWeatherData_Input[StartMonth]=StartMonth
    HEMSWeatherData_Input[StartDay]=StartDay
    HEMSWeatherData_Input[StartTime]=StartTime
    HEMSWeatherData_Input[EndYear]=EndYear
    HEMSWeatherData_Input[EndMonth]=EndMonth
    HEMSWeatherData_Input[EndDay]=EndDay
    HEMSWeatherData_Input[EndTime]=EndTime

    if WeatherDataType==1: # We do not have Weather Data File
        [HEMSWeatherData_Output] = WeatherData_Extractor(HEMSWeatherData_Input,Simulation_Params,WeatherData_FileName);
    elif (WeatherDataType==2): # We have Weather Data File
        load(strcat(WeatherData_FileName,'.mat'))    #load weather file
    
    # Load Data Extraction

    #Type=1; % Type of Load Data Extraction
    if LoadDataType==1: # We do not have Load Data File
        [PecanStreet_Data_Output] = PecanStreet_Data_Extractor(HEMSWeatherData_Input,Simulation_Params,LoadDataFolder_Path,N_House_Vector,SimulationType,LoadData_FileName);
    elif LoadDataType==2: # We already have Load Data File
        load(strcat(LoadData_FileName,'.mat'));
    
    # Basic Computation

    #-------------------- Creating Community_Params Struct -------------------%
    Community_Params = {}
    Community_Params[N_House]=N_House
    Community_Params[N_PV_Bat]=N_PV_Bat
    Community_Params[N_Bat]=N_Bat
    Community_Params[N_PV]=N_PV
    Community_Params[N_None]=N_None
    
    #------------------- From Extracted Weather Data -------------------------%
    
    Ws = HEMSWeatherData_Output[Ws]
    T_am = HEMSWeatherData_Output[T_am]
    GHI = HEMSWeatherData_Output[GHI]
    DNI = HEMSWeatherData_Output[DNI]
    DateTimeVector = HEMSWeatherData_Output[DateTimeVector]
    DateTime_Matrix = HEMSWeatherData_Output[DateTime_Matrix]
    Simulation_Steps_Total = len(DateTimeVector)
    
    #------------------------ From Extracted Load Data -----------------------%

    # Getting Renewable Source Data (adding -1 to indexes because matlab is 1 indexed and python is 0 indexed)
    SolarGen_Data=PecanStreet_Data_Output[:,4:6,:]
    
    Battery_ChargerDischarge_Data=PecanStreet_Data_Output[:,7-1,:]
    
    EVCharging_Data=PecanStreet_Data_Output[:,7+1-1:9,:]
    
    E_LoadData=PecanStreet_Data_Output[:,:,:]
    
    # Making Negatives (-) = 0 in LoadData
    #goes through all values in certain columns and takes out all negative values
    #E_LoadData(E_LoadData[:,9+1-1:end,:]<0)=0
    for i in range(E_LoadData.shape[0]):
        for j in range(E_LoadData.shape[1]):
            for k in range(9, E_LoadData.shape[2]):
                if E_LoadData[i,j,k] < 0:
                    E_LoadData[i,j,k] = 0
    
    
    # Creating 8 Level Priority Load Data
#rewrite to same functionality as sum function us np.sum 
    E_Load_P1 = np.sum(E_LoadData[:,:,9:21]) # Priority Level1 Sum column 9-20
    E_Load_P2 = np.sum(E_LoadData[:,:,21:26]) # Priority Level2 Sum column 21-25
    E_Load_P3 = np.sum(E_LoadData[:,:,26:29]) # Priority Level3 Sum column 26-28
    E_Load_P4 = np.sum(E_LoadData[:,:,29:36]) # Priority Level4 Sum column 29-35
    E_Load_P5 = np.sum(E_LoadData[:,:,36:42]) # Priority Level5 Sum column 36-41
    E_Load_P6 = np.sum(E_LoadData[:,:,42:48]) # Priority Level6 Sum column 42-47
    E_Load_P7 = np.sum(E_LoadData[:,:,48-51]) # Priority Level7 Sum column 48-50
    E_Load_P8 = np.sum(E_LoadData[:,:,51-57]) # Priority Level8 Sum column 51-56 column 57 is house number
    
    #does this concatenate the matricies?
    E_LoadData=[E_LoadData[:,0:9,:], E_Load_P1, E_Load_P2, E_Load_P3, E_Load_P4, E_Load_P5, E_Load_P6, E_Load_P7, E_Load_P8];

    # Creating E_Load_Desired from LoadData (Summing all loads for a given house)
    E_Load_Desired_Array = np.sum(E_LoadData[:,:,9:E_LoadData.shape[2]])
    
    # Creating E_Load_Desired from E_Load_Array
    E_Load_Desired = []
    for i in range(1,N_House):
        E_Load_Desired.append(E_Load_Desired_Array[:,:,i])
    
    # Community-House Parameter Generation
    
    [HEMSPlant_Params,HEMSHouse_Params] = HEMS_CommunityHouse_Parameter_Generator(Community_Params,Simulation_Params);
    
    # Initial States,Disturbance and Control Struct Creation

    