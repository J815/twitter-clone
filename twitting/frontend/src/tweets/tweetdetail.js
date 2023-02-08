import React, {useState} from "react"
import { ActionButton } from "./tbutton"
import { UserDisplay, UserPicture } from "../profiles/parts"


export function ParentTweet(props){
    const {tweet}= props
    return tweet.parent ? <div>
        <Tweet isRetweet retweeter={props.retweeter} hideAction className={' '} tweet= {tweet.parent} />
    </div> : null
}

export function Tweet(props) {
    const {tweet, didRetweet, hideAction, isRetweet, retweeter} = props
    const [tweetAction, setTweetAction]= useState(props.tweet ? props.tweet : null)
    let className= props.className ? props.className: 'col-10 mx-auto col-md-6'
    className= isRetweet=== true ? `${className} mb-2 p-2 border rounded` : className
    const path= window.location.pathname
    const match= path.match(/(?<id>\d+)/)
    const urlTweetId= match ? match.groups.id : -1
    const isDetail= `${tweet.id}` ===`${urlTweetId}`

   const handleLink =(event) =>{
       event.preventDefault()
       window.location.href= `/${tweet.id}`
   }

   const handleAction= (newTweetAction, status) =>{
       if (status === 200){
           setTweetAction(newTweetAction)
       }else if(status === 201){
           if(didRetweet){
               didRetweet(newTweetAction)
           }
       }
   }
   return <div className={className}>
      {isRetweet=== true && <div className='mb-3'>
          <span className='small text-muted'>Retweet by <UserDisplay user={retweeter} /></span>
          </div>}
     
     <div className='d-flex'>
         <div className=''>
                 <UserPicture user={tweet.user} />
         </div>
        <div className='col-11'>  
            <div>
                <p><UserDisplay includeFullName  user={tweet.user} /></p>
                <p className='my-1 p-1'>{tweet.content}</p>
                <ParentTweet tweet= {tweet} retweeter={tweet.user} />
            </div>
           <div className='px-0'>
             {(tweetAction && hideAction !== true) && <React.Fragment>
                <ActionButton tweet={tweetAction} didAction={handleAction} action={{type:"like", display:"likes"}}/>
                <ActionButton tweet={tweetAction} didAction={handleAction} action={{type:"unlike", display:"unlike"}}/>
                <ActionButton tweet={tweetAction} didAction={handleAction} action={{type:"retweet", display:"Retweet"}}/>
              </React.Fragment>
             }
              {isDetail === true ? null : <button className='btn btn-outline-primary btn-sm' onClick={handleLink}>View</button>}
           </div>
         </div>

     </div>
   </div>
}
