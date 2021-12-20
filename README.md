# Does a master's degree lead to a higher salary in STEM jobs?
Jupyter notebook containts the data manipulation and EDA
- Drop null rows of education since it is the main variable I am evaluating
- Fill 'level','tag' and 'company' missing values with the mode
- Fill 'gender' missing values with a random assingment of male/female
![image](https://user-images.githubusercontent.com/96037819/146714466-b519be69-d370-4b4c-8ec9-5f42aca01034.png)
<br>
Since our focus is on whether master's degree leads to a higher salary, we remove employee data containing people who have more than 25 years of experience.
When someone has a lot of experience in a field, his/her qualifications will not impact the salary as much as the work they have done in the field.
Initial boxplot shows us that those who have a master's degree have a higher median salary than those with a bachelor's degree.
The same trend holds true across various levels of experience.
<br>
Plot a map that shows the average salary by state in the United States.
![image](https://user-images.githubusercontent.com/96037819/146713411-027d11c2-81ff-449a-8a47-875512dc55c0.png)
## Hypothesis testing
Null Hypothesis : The salary of a person who holds a Masters degree is equal to the salary of a person who does not have a Masters degree
Alternate Hypothesis : The salary of a person who holds a Masters degree is greater than the salary of a person who does not have a Masters degree
<br>
First regression model has master's degree, years of pexperience and job location as the independent variables.
![image](https://user-images.githubusercontent.com/96037819/146713515-eb77bf2c-f8c4-41f5-9071-9b194b6a7c6d.png)
Controlling for years of experience, gender, and job location, the expected total yearly compensation increases by 6.96% for employees with a Master’s Degree, in comparison to employee’s without a Master’s Degree.
<br>
## Does a master's degree lead to a higher salary for Data Scientist/Business analyst roles?
![image](https://user-images.githubusercontent.com/96037819/146714560-4866bebe-d363-4972-a642-63f784fa4e4c.png)
![image](https://user-images.githubusercontent.com/96037819/146714575-93973e9f-1827-4bbd-b0a4-41764735e545.png)
<br>
Regression analysis with master's degree and years of experience as independent variables gives us the following output
![image](https://user-images.githubusercontent.com/96037819/146713730-b11d9293-4a63-4a5b-84ad-4c33f8e5279c.png)
The p-value for master's degree is 0.398
We cannot reject the null hypothesis that master’s degree does not lead to higher total compensation for data science/business analyst roles.

## Dashboard creation using plotly dash
The dashboard_Final.py contains the dashboard created using the data.
Please download all the csv files attached to ensure the dashboard works properly.
- Clustering analysis using k-means was performed to segment the data into 4 clusters. Elbow method was used to identify optimum k value.
- The dashboard shows salary distribution across states, among different genders, and among different experience levels. The filter level is the level of Education.
- Tables tab gives us the annual salary for the top 10 states having the highest total annual compensation.
