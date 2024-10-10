# Credit-Risk-Modeling-Application


Hello Data Scientist, my credit risk modeling application is here to assess the hashtag#creditworthiness of loan applicants by predicting the probability of default, calculating a credit score, and assigning a rating like hashtag#Excellent, hashtag#Good, hashtag#Average, or hashtag#Poor. Let’s dive into how it works:
🛠️ hashtag#ModelOverview
🔍 hashtag#DataPreprocessing:
Your model uses a variety of hashtag#financial and hashtag#personal details such as hashtag#age, hashtag#income, hashtag#loanamount, hashtag#loantenure, and more.
Categorical variables like hashtag#residencetype and hashtag#loanpurpose are transformed into numeric values using hashtag#onehotencoding 🔢.
Key features are scaled using a hashtag#MinMaxScaler to keep everything consistent and optimized for the model’s performance 🚀.
📈 hashtag#PredictionModel:
At its core, your model uses hashtag#LogisticRegression, trained on historical data, to predict the probability of default for each applicant 🧠.
It computes a weighted sum of features, passes it through a hashtag#logisticfunction, and voila! You get the default probability 🎯.
This probability is converted into a hashtag#creditscore ranging from 300 to 900.
🔢 hashtag#CreditScoreCalculation:
The credit score is derived from the non-default probability, scaled between #300 (base score) and #900 (maximum score) 📊.
Based on the score, the model assigns a rating:
hashtag#Poor: 300-499 😟
hashtag#Average: 500-649 😐
hashtag#Good: 650-749 🙂
hashtag#Excellent: 750-900 😃
👥 hashtag#UserInteraction
The app supports both hashtag#ManualInput 📝 and hashtag#BatchProcessing 📂 via file upload.
For each applicant, the app calculates and displays the hashtag#defaultprobability, hashtag#creditscore, and hashtag#rating. You can even visualize these using various hashtag#charttypes 📊🎨.
🏁 hashtag#Conclusion
Your model makes use of hashtag#LogisticRegression to assess credit risk by analyzing a range of hashtag#financial and hashtag#personalfactors. By processing the data into a default probability, credit score, and rating, it helps in making smart, informed lending decisions 💡. With features like hashtag#onehotencoding and hashtag#scaling, the data is primed for accuracy and reliability in predictions 🔧🔍.

