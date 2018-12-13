#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (\$645-675) underperformed compared to schools with smaller budgets (<\$585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "schools_complete.csv"
student_data_to_load = "students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)
student_data.head()

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[2]:


#Calculate the total number of schools
totalSchool=school_data.school_name.count()
totalSchool


# In[3]:


# Calculate the total number of students
student_data_renamed=student_data.rename(index=str, columns={"Student ID":"Student_ID"})
student_data_renamed.head(10)
totalStudents=student_data_renamed.Student_ID.count()
totalStudents


# In[4]:


#Calculate the total budget
totalBudget=school_data.budget.sum()
totalBudget


# In[5]:


#Average Math Score
avgMathScore=student_data_renamed.math_score.mean()
avgMathScore


# In[6]:


#Calculate the average reading score
avgReadingScore=student_data_renamed.reading_score.mean()
avgReadingScore


# In[7]:


#Overall Pass Rate
overallPassRate=(avgMathScore+avgReadingScore)/2
overallPassRate


# In[8]:


# Calculate the percentage of students with a passing math score (70 or greater)
student_data_renamed['MathPass'] = (student_data_renamed.math_score>=70)
student_data_Math_pass=student_data_renamed.loc[student_data_renamed["MathPass"]==True,:]
countMathPass=student_data_Math_pass.Student_ID.count()
mathPassPct=countMathPass/totalStudents*100
mathPassPct


# In[9]:


# Calculate the percentage of students with a passing reading score (70 or greater)
student_data_renamed['ReadPass'] = (student_data_renamed.reading_score>=70)
student_data_reading_pass=student_data_renamed.loc[student_data_renamed["ReadPass"]==True,:]
countReadPass=student_data_reading_pass.Student_ID.count()
readPassPct=countReadPass/totalStudents*100
readPassPct


# In[10]:


#Create a dataframe to hold the above results
Final=pd.DataFrame(
    [[totalSchool,totalStudents,totalBudget,avgMathScore,avgReadingScore,mathPassPct,readPassPct,overallPassRate]],
    columns =['Total Schools','Total Students', 'Total Budget','Average Math Score','Average Reading Score','%Pass Math','%Pass Reading','Overall Passing Rate'])
Final.head()


# ## School Summary
# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# #* School Name   * School Type   * Total Students
# 

# In[11]:



school_types = school_data.set_index(["school_name"])["type"]
school_types
Total_Students = school_data_complete["school_name"].value_counts()
Total_Students
total_Budget=school_data.groupby(["school_name"]).mean()["budget"]
total_Budget
Per_Student_Budget= total_Budget/Total_Students

avg_Math_Score=school_data_complete.groupby(["school_name"]).mean()["math_score"]
avg_Math_Score                           

avg_Reading_Score=school_data_complete.groupby(["school_name"]).mean()["reading_score"]
avg_Reading_Score

sch_pass_Math=school_data_complete[(school_data_complete["math_score"]>=70)]
sch_pass_Math.head()
sch_pass_Math_pct=sch_pass_Math.groupby(["school_name"]).count()["student_name"]/Total_Students *100

sch_pass_Read=school_data_complete[(school_data_complete["reading_score"]>=70)]
sch_pass_Read_pct=sch_pass_Read.groupby(["school_name"]).count()["student_name"]/Total_Students *100

Overall_Pass=(sch_pass_Math_pct+sch_pass_Read_pct)/2

school_summary = pd.DataFrame({"School_Type": school_types,
                               "Total_Students": Total_Students,
                               "Total_Budget":total_Budget,
                                "Per_Student_Budget":Per_Student_Budget,
                                 "Average_Math_Score":avg_Math_Score,
                                  "Average_Reading_Score":avg_Reading_Score,
                                   "%Passing_Math" : sch_pass_Math_pct,
                                   "%Passing_Reading" :sch_pass_Read_pct,
                                   "Overall_Pass":Overall_Pass
                                  })

school_summary


# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[12]:


school_summary = school_summary.sort_values("Overall_Pass", ascending=False)
school_summary.head()


# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[13]:


school_summary.tail()


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[21]:




only_9th_math=student_data[(student_data["grade"]=="9th")]
only_10th_math=student_data[(student_data["grade"]=="10th")]
only_11th_math=student_data[(student_data["grade"]=="11th")]
only_12th_math=student_data[(student_data["grade"]=="12th")]
only_9th_math= only_9th_math.groupby(["school_name"]).mean()["math_score"]
only_10th_math= only_10th_math.groupby(["school_name"]).mean()["math_score"]
only_11th_math= only_11th_math.groupby(["school_name"]).mean()["math_score"]
only_12th_math= only_12th_math.groupby(["school_name"]).mean()["math_score"]

math_Score_byGrade=pd.DataFrame({"9th":only_9th_math, "10th":only_10th_math,"11th":only_11th_math,"12th":only_12th_math})
math_Score_byGrade.index.name=None
math_Score_byGrade


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[23]:


only_9th_reading=student_data[(student_data["grade"]=="9th")]
only_10th_reading=student_data[(student_data["grade"]=="10th")]
only_11th_reading=student_data[(student_data["grade"]=="11th")]
only_12th_reading=student_data[(student_data["grade"]=="12th")]
only_9th_reading= only_9th_reading.groupby(["school_name"]).mean()["reading_score"]
only_10th_reading= only_10th_reading.groupby(["school_name"]).mean()["reading_score"]
only_11th_reading= only_11th_reading.groupby(["school_name"]).mean()["reading_score"]
only_12th_reading= only_12th_reading.groupby(["school_name"]).mean()["reading_score"]

reading_Score_byGrade=pd.DataFrame({"9th":only_9th_reading, "10th":only_10th_reading,"11th":only_11th_reading,"12th":only_12th_reading})
reading_Score_byGrade.index.name=None
reading_Score_byGrade


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[16]:


# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$616-645", "$646-675"]

school_summary["Spending Ranges(Per Student)"] = pd.cut(school_summary["Per_Student_Budget"], spending_bins, labels=group_names)

avg_Math_Score = school_summary.groupby(["Spending Ranges(Per Student)"]).mean()["Average_Math_Score"]
avg_Reading_Score = school_summary.groupby(["Spending Ranges(Per Student)"]).mean()["Average_Reading_Score"]
sch_pass_Math_pct = school_summary.groupby(["Spending Ranges(Per Student)"]).mean()["%Passing_Math"]
sch_pass_Read_pct = school_summary.groupby(["Spending Ranges(Per Student)"]).mean()["%Passing_Reading"]
Overall_Pass = (sch_pass_Math_pct+sch_pass_Read_pct)/2

school_summary_bySpend = pd.DataFrame({"Average Math Score" : avg_Math_Score,
                                     "Average Reading Score" : avg_Reading_Score,
                                     "% Passing Math" : sch_pass_Math_pct,
                                     "% Passing Reading" : sch_pass_Read_pct,
                                      "Overall Pass ":      Overall_Pass
                                      })



school_summary_bySpend
   


# In[ ]:





# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[24]:


# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


school_summary["Scores by Size"] = pd.cut(school_summary["size"], size_bins, labels=group_names)

avg_Math_Score = school_summary.groupby(["Scores by Size"]).mean()["Average_Math_Score"]
avg_Reading_Score = school_summary.groupby(["Scores by Size"]).mean()["Average_Reading_Score"]
sch_pass_Math_pct = school_summary.groupby(["Scores by Size"]).mean()["%Passing_Math"]
sch_pass_Read_pct = school_summary.groupby(["Scores by Size"]).mean()["%Passing_Reading"]
Overall_Pass = (sch_pass_Math_pct+sch_pass_Read_pct)/2

school_summary_bySize = pd.DataFrame({"Average Math Score" : avg_Math_Score,
                                     "Average Reading Score" : avg_Reading_Score,
                                     "% Passing Math" : sch_pass_Math_pct,
                                     "% Passing Reading" : sch_pass_Read_pct,
                                      "Overall Pass ":      Overall_Pass
                                      })



school_summary_bySize
   


# In[ ]:





# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[18]:


#perform the above group by school type 
avg_Math_Score = school_summary.groupby(["School_Type"]).mean()["Average_Math_Score"]
avg_Reading_Score = school_summary.groupby(["School_Type"]).mean()["Average_Reading_Score"]
sch_pass_Math_pct = school_summary.groupby(["School_Type"]).mean()["%Passing_Math"]
sch_pass_Read_pct = school_summary.groupby(["School_Type"]).mean()["%Passing_Reading"]
Overall_Pass = (sch_pass_Math_pct+sch_pass_Read_pct)/2

school_summary_bySchooltype = pd.DataFrame({"Average Math Score" : avg_Math_Score,
                                     "Average Reading Score" : avg_Reading_Score,
                                     "% Passing Math" : sch_pass_Math_pct,
                                     "% Passing Reading" : sch_pass_Read_pct,
                                      "Overall Pass ":      Overall_Pass
                                      })



school_summary_bySchooltype


# In[ ]:




