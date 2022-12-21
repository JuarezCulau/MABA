You can use the model already trained and available with MABA. However, that's not recommended, so you can either train your own model or use [DeepLabCut](https://github.com/DeepLabCut/DeepLabCut)
Creating your own model is recommended because it will grant more precision for the analysis, since your environment is not the same used to train our model. 

I used ResNet50 for the model trained to work with MABA, so you may have to modify the Model.py file if you choose another methodology.
To make it easier, MABA was created to work with exported models from DeepLabCut. You can train your models following their protocols.
There is only one important thing to note, you have to follow the same order of points that we did with MABA if you don't want to modify any code. 

![DALL·E 2022-10-24 22 29 57 - A mice seen from above with translucent skeleton, anatomy art](https://user-images.githubusercontent.com/88636064/208991665-41c6c404-f30b-495a-9ed8-70d4e05e08e5.png)

# Once you have trained your model, export and you are ready to use it on MABA!
