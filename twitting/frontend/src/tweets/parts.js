import React, {useEffect, useState} from 'react'

import { TweetCreate } from './tcreate'
import { Tweet } from './tweetdetail'
import { FeedList } from './feed'
import { tweetDetail } from '../lookup/parts'
import { TweetList } from './tlist'

export function FeedElement(props){
    const [newTweet, setNewTweet]= useState([])
    const canTweet= props.canTweet=== "false" ? false : true
    const handleNewTweet= (newTwet)=>{
        let newTweetList= [...newTweet]
        newTweetList.unshift(newTwet)
        setNewTweet(newTweetList)
    }
    return <div className={props.className}>
             {canTweet=== true && <TweetCreate didTweet={handleNewTweet} className= 'col-10 mx-3 my-3' />}       
           <FeedList newTweet={newTweet} {...props}/>
     </div>
}

export function TweetElement(props){
    const [newTweet, setNewTweet]= useState([])
    const canTweet= props.canTweet=== "false" ? false : true
    const handleNewTweet= (newTwet)=>{
        let newTweetList= [...newTweet]
        newTweetList.unshift(newTwet)
        setNewTweet(newTweetList)
    }
    return <div className={props.className}>
             {canTweet=== true && <TweetCreate didTweet={handleNewTweet} className= 'col-10 mx-3 my-3' />}       
           <TweetList newTweet={newTweet} {...props}/>
     </div>
}

export function TweetDetailElement(props){
     const {id}= props
     const [didLookup, setDidLookup]= useState(false)
     const [tweet, setTweet]= useState(null)
     const backendLookup=(response, status)=>{
         if(status=== 200){
             setTweet(response)
         }else{
             alert("There was an error finding your tweet")
         }
     }
     useEffect(()=>{
         if(didLookup=== false){
             tweetDetail(id, backendLookup)
             setDidLookup(true)
         }
     },[id, didLookup, setDidLookup])
    
     return tweet=== null ? null : <Tweet tweet={tweet} className={props.className} />
 }