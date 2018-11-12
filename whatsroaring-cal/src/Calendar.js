import React, { Component } from 'react'
import axios from 'axios'
import './App.css'
import BigCalendar from 'react-big-calendar'

import 'react-big-calendar/lib/css/react-big-calendar.css'
import moment from 'moment'


const localizer = BigCalendar.momentLocalizer(moment)
const url = 'http://127.0.0.1:8000/getEvents'

class Calendar extends Component {
  constructor(...args) {
    super(...args)
    this.state = { events:[] }
  }

  componentDidMount() {
    axios.get(url).then(res => {
      const posts = JSON.parse(res.data.Events_JSON)
      const events = [];
      posts.forEach(function(post){
        events.push({start: new Date(post.fields.start_datetime), title: post.fields.name, 
          end: new Date(post.fields.end_datetime),
          desc: post.fields.description});
      });
      console.log(posts)
      this.setState({ events });
    })
  }

  render() {
    return (
      <div className='Calendar'>
        <BigCalendar
          localizer={localizer}
          events={this.state.events}
          defaultView={BigCalendar.Views.MONTH}
          onSelectEvent={event => alert(event.desc)}
          // titleAccessor="fields.name"
          // startAccessor="fields.start_datetime"
          // endAccessor="fields.end_datetime"
        />
      </div>
    )
  }
}

export default Calendar;