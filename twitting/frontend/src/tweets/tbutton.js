
import React from "react"
import {tweetAction} from '../lookup/parts'


export function ActionButton(props){
    const {tweet, action, didAction}= props
    const likes= tweet.likes ? tweet.likes: 0
    const className= props.className ? props.className:'btn btn-outline-primary btn-sm'
    const actionDisplay = action.display ? action.display: 'Action'

    const actionBackendEvent= (response, status)=>{
        if ((status=== 200 || status=== 201) && didAction){
            didAction(response, status)
        }
    }
    const handleClick= (event)=>{
        event.preventDefault()
        tweetAction(tweet.id, action.type, actionBackendEvent)
    }
       const display= action.type=== "like" ? `${likes} ${actionDisplay}`: actionDisplay
       return <button className={className} onClick={handleClick}>{display}</button>
}