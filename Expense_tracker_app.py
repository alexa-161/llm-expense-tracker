#https://www.freecodecamp.org/news/build-smart-expense-tracker-with-python-and-llms/

#Purpose of this file is for testing and background logic


#Data Cleaning and printing
import pandas as pd

df = pd.read_csv("expense_data_1.csv")
print(df.head()) #printing data frame
data=df[["Date", "Category","Note","Amount","Income/Expense",]] #Cleaning df, choosing which to keep
print(data.head())#print new data

#Define a function that appends data into our dataframe, consisting of details
#such as date, category, note...,exp type
def add_expense(date, category, note, amount, exp_type="Expense"): #defining parameter, js means if user dont provide value for exp_type, auto use Expense
    global data #ensures that new expense is added to main dataset and not js a temp copy
    new_entry={ #created dictionary for new row, match columns of data we want to appned to ones alr exissting in our dataset
        "Date":date,
        "Category":category, #dictionary uses : not =
        "Note":note,
        "Amount":amount,
        "Income/Expense":exp_type #js write variable name
    }
    new_df = pd.DataFrame([new_entry])
    data = pd.concat([data, new_df], ignore_index=True) #pandas ver dont support; data= data.append(new_entry, ignore_index=True) #ensures row number stay clean and sequential, gives new row next avail number instead of resetting to 0
    print(f"Added:{note}-{amount} ({category})")

add_expense("2025-08-22 19:30","Food","Shawarma",2500,"Expense")
add_expense("2025-08-23 20:00","Transport","Bus",1000,"Expense")
add_expense("2025-08-24 11:00","Entertainment","Amusement park",400,"Expense")



#Define a function for viewing recent expenses (returns bottom/last row-> use.tail())
def view_expenses(n=5):
    return data.tail(n)#returns last n number of rows
print(view_expenses(5))



#Define a function to summarize spending
def summarize_expenses(by="Category"):
    summary=data[data["Income/Expense"]=="Expense"].groupby(by)["Amount"].sum()# grpby applies to expenses onto category(take categories under expenses), split data in Expense into its own category; sum applies to Amount column
    return summary.sort_values(ascending=False) #functions that sorts asc order; False=sort descending                                                            #data["Income/Expense"] in pandas mean give me entire column named that
                                                #When filtering: data[data["ColumnName"] == "ValueYouWant"] 
print(summarize_expenses())                     #["Expense"]-> actual word expense, [Expense]->python looks for var named Expense


#Make it smart using LLMs(Auto-categorization into most relevant category)
from openai import OpenAI
client=OpenAI(api_key="YOUR_API_KEY")

def auto_categorize(note): # """ multiliner str
    prompt= f"""  
    Categorize this expense note into one of these categories: Food, Transportation, Entertainment,
    Other. 
    Note:{note}
    """
    try:
        response= client.chat.completions.create( #sends request to OpenAI to generate a response
            model="gpt-4o-mini", #model we r using
            messages=[{"role":"user", "content": prompt}], #role= who said it; user=u, content= what was actually said
            temperature=0 #controls how creative AI is; scale:0 to 2(higher=more random/creative); choose 0 for consistency
        )
        return response.choices[0].message.content.strip() #strip() removes white space from start/end from GPT response content 
    except Exception as e: #if any error occur in try block, store error of any type in a var called e
        return "Other" #return string Other

# pandas pattern that automatically fills in missing categories.    
data['Category']= data.apply( #assigns new values to 'Category' column and run function apply 
    lambda row: auto_categorize(row['Note']) if pd.isna(row['Category']) else row['Category'], #pd.isna() panda funct that checks if value is empty(returns True)
                                                                                                #For each row, look at the Category. If it's empty/missing, then run auto_categorize() on the Note to figure it out. But if Category already has a value, just keep that value.
    axis=1 #function apply across columns; axis=0: mean apply to vertical columns
)
print(data[['Note','Category']].head(10)) # selects only two columns from your dataframe: 'Note' and 'Category'.
                                          #.head(10) shows first 10 rows of selected columns


#USE MATPLOTLIB TO BUILD A PIECHART & BAR CHART
import matplotlib.pyplot as plt #importing package matplotlib; .pyplot file inside that folder; giving shorter nickname plt
expense_summary= data[data['Category']!='Income'].groupby('Category')['Amount'].sum() #filtering data categories to exclude Income
                                                                                        #.groupby('Category') splits your data into groups based on unique categories
#PIE CHART
plt.figure(figsize=(6,6)) #creating a canvas w dimensions (width,ht), whr chart will be drawn                                                                                       #['Amount].sum() in each grp select amount column and apply sum to it
expense_summary.plot.pie(autopct='%1.1f%%',startangle=90)
#.plot.pie() plotting command
#formats % labels
#signals start and end of specifer
#1.1f, convention for pie charts, shows no. 1 digit before and 1 dig after decimal
#startangle=90 rotates starting point, first slice is at 90deg
plt.title('Expenses breakdown by Category')
plt.ylabel('')#piecharts no y axis
plt.show()

#BAR CHART
plt.figure(figsize=(8,6))
expense_summary.plot(kind='bar',color="pink")
plt.title('Expense Category breakdown')
plt.xlabel("Category")
plt.ylabel("Amount")
plt.show()




