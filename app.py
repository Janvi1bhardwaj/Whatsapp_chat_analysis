import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
st.sidebar.title("Whatsapp Chat Analysis")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    # dataframe
    df=preprocessor.preprocess(data)
    # st.dataframe(df)
    
    # fetch unique user
    user_list=df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)
    
    # stats.....
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistic")
        num_msg,words,num_media_msg,num_links=helper.fetch_stats(selected_user,df)
        
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Message")
            st.title(num_msg)
        with col2:
            st.header("Total Word")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_msg)
        with col4:
            st.header("Link Shared")
            st.title(num_links)
            
    # monthly_timeline
    timeline=helper.monthly_timeline(selected_user,df)
    st.title("Monthly Timeline")
    
    fig,ax=plt.subplots()
    plt.plot(timeline["time"],timeline["msg"],color="green")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # daily_timeline
    st.title("Daily Timeline")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['msg'], color='black')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    
    # activity map
    st.title('Activity Map')
    col1,col2 = st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day = helper.week_activity_map(selected_user, df)
        
        chart_data = pd.DataFrame(busy_day).reset_index()
        chart_data.columns = ['Day', 'Messages']
        
        chart_data.index = range(len(chart_data))        
        st.bar_chart(chart_data.set_index('Day')['Messages'])
        
    with col2:
        st.header("Most busy month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    
    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap,yticklabels=False)
    st.pyplot(fig)
    
    # busy user.....
    if selected_user=="Overall":
        st.title("Most Busy user")
        
        x,new_df=helper.most_busy_users(df)
        fig,ax=plt.subplots()
        
        col1,col2=st.columns(2)
        with col1:
            ax.bar(x.index,x.values,color="red")
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
        with col2:
            st.dataframe(new_df)
    
    # wordcloud......
    st.title("WordCloud")
    df_wc=helper.create_wordcloud(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    
    
    # 20 words
    most_common_df=helper.most_common_words(selected_user,df)
    fig,ax=plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation=45)
    
    st.title("Most Common Words")
    st.pyplot(fig)
    
    # emoji analysis
    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df['Count'], labels=emoji_df['Emoji'], autopct='%1.1f%%')
        st.pyplot(fig)
    