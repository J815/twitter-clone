import React, {useEffect, useState} from 'react'

import { UserDisplay, UserPicture } from './parts'
import { profileDetail, profileFollowToggle } from '../lookup/parts'
import {DisplayCount} from './utils'


function ProfileDisplay(props){
    const {user, didFollowToggle, profileLoading}= props
    let currentstate= (user && user.is_following) ? "Unfollow": "Follow"
    currentstate= profileLoading ? "Loading..." : currentstate
    const followToggle= (event) =>{
        event.preventDefault()
        if(didFollowToggle && !profileLoading){
            didFollowToggle(currentstate)
        }
    }
    return user ? <div className='py-5 mx-auto col-md-6'>
        <p className='item'><UserPicture user={user} hideLink /></p>
        <p className='item'><UserDisplay user={user} includeFullName hideLink /></p>
        <p className='item'>{user.location}</p>
        <p className='item'><DisplayCount>{user.follower_count}</DisplayCount> {user.follower_count=== 1 ? "follower" : "followers"}</p>
        <p className='item'><DisplayCount>{user.following_count}</DisplayCount> following</p>
        <p className='item'>{user.bio}</p>
        <p className='item'> <button className='btn btn-primary' onClick={followToggle}>{currentstate}</button></p>
    </div> : null
}

export function ProfileDisplayElement(props){
    const {username}= props
    const [didLookup, setDidLookup]= useState(false)
    const [profile, setProfile]= useState(null)
    const [profileLoading, setProfileLoading]= useState(false)
    const backendLookup= (response, status)=>{
        if(status=== 200){
            setProfile(response)
        }
    }
    useEffect(()=>{
        if(didLookup=== false){
            profileDetail(username, backendLookup)
            setDidLookup(true)
        }
    }, [username, didLookup, setDidLookup])

    const newFollow= (actionVerb)=> {
        profileFollowToggle(username, actionVerb, (response, status)=>{
            if(status=== 200){
                setProfile(response)
            }
            setProfileLoading(false)
        })
        setProfileLoading(true)
    }
    return didLookup=== false ? "Loading..." : profile ? <ProfileDisplay user={profile} didFollowToggle={newFollow} profileLoading={profileLoading} /> : null
}