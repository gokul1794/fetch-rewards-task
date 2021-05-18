#Fetch Take home test

1. Review unstructured JSON data and diagram a new structured relational data model

	The data model is stored as datamodel.png 
    
2. Generate a query that answers a predetermined business question

	The answers to the questions are in the business-questions-sql folder named business-questions.sql, the outputs are also stored in the word document there.
    
3. Generate a query to capture data quality issues against the new structured relational data model
	
	Data Quality related query is present in the dataquality sql file. It is also present in the word document.
    
4. Write a short email or Slack message to the business stakeholder

	Stakeholder email is present in the docs folder.

##Additional Notes -
1. The file etl, contains the initial loading, cleaning and transforming. It cleans and generates csv files which were then bulk inserted into postgres for analysts. <br>
2. Change the path in the py file to your path to run the program, in hindsight I should've probably given relative paths. <br>
3. The top 5 brand query is written for january because March, April, May did not have any values. <br>
4. The create scripts in business-questions can be used to create the tables, the clean csv files are in data/CleanFiles.
5. All the csv headers are in Camel Case, make sure you change them to like_this before you insert. 