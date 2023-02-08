import React, {useEffect, useState} from 'react'
import { existing_tweet} from '../lookup/parts'

import { Tweet } from './tweetdetail'

export function TweetList(props){
     const [tweetInitial, setTweetInitial] = useState([])
     const [tweets, setTweets]= useState([])
     const [tweetSet, setTweetSet]= useState(false)
     const [nextUrl, setNextUrl]= useState(null)
     useEffect(() =>{
       const finalList= [...props.newTweet].concat(tweetInitial)
       if(finalList.length !== tweets.length){
          setTweets(finalList)
       }
     }, [props.newTweet, tweets, tweetInitial])
     
     useEffect(() => {
         if(tweetSet === false){  
          const tweetListLookup = (response, status)=>{
              if (status=== 200){
                setNextUrl(response.next)
                setTweetInitial(response.results)
                setTweetSet(true)
            }else{
                alert("There was an error")
            }
          }
           existing_tweet(props.username, tweetListLookup)
     }
    }, [tweetInitial, tweetSet, setTweetSet, props.username])

    const tweetDidRetweet= (newTweet)=>{
        const retweetInitial= [...tweetInitial]
        retweetInitial.unshift(newTweet)
        setTweetInitial(retweetInitial)
        const finalTweet= [...tweets]
        finalTweet.unshift(tweets)
        setTweets(finalTweet)
    }
    const loadNext=(event) =>{
        event.preventDefault()
        if (nextUrl !== null){
            const loadNextResponse = (response, status)=>{
                if(status=== 200){
                    setNextUrl(response.next)
                    const newTweets= [...tweets].concat(response.results)
                    setTweetInitial(newTweets)
                    setTweets(newTweets)
                }else{
                    alert("There was an error")
                }
            }
            existing_tweet(props.username, loadNextResponse, nextUrl)
        }
    }
    
    return <React.Fragment>{tweets.map((item, index)=>{
        return <Tweet didRetweet={tweetDidRetweet}  tweet={item} className='my-5 px-3 py-4 col-11 mx-auto border bg-white text-dark'
         key={`${index}-{item.id}`}/>
    })}
    {nextUrl!== null && <button onClick={loadNext} className='btn btn-outline-primary'>Load More</button>}
    </React.Fragment>
}
