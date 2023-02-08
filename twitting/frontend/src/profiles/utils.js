import React from "react"
import numeral from 'numeral'

export function DisplayCount(props){
    return <span className='px-2'>{numeral(props.children).format("0a")}</span>
}