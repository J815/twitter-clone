import React from 'react'
import { createTweet } from '../lookup/parts'

export function TweetCreate(props){
    const textAreaRef= React.createRef()
    const {didTweet}= props
    
    const backendUpdate = (response, status) =>{
        if(status=== 201){
           didTweet(response)
        }else{
            console.log(response)
            alert("An error occured, please try again")
        }
     }
     const handleSubmit= (event) => {
         event.preventDefault()
         const newElement = textAreaRef.current.value
         createTweet(newElement, backendUpdate) 
         textAreaRef.current.value= ''
     }
     return <div className={props.className}>
                  <form onSubmit= {handleSubmit}>
                      <textarea ref= {textAreaRef} required= {true} className= 'form-control' name= 'tweet'>

                      </textarea>
                      <button type= 'submit' className= 'btn btn-primary my-3'>Tweet</button>
                  </form>    
    </div>
}