import React from 'react'

import { useSelector } from 'react-redux'

export const ProfileComponent = props => {
  const user = useSelector(state => state.user.user)

  return (
    <div className="card">
      <div className="card-body">
        <div className="h5">@{user.username}</div>
        <div className="h7 text-muted">Fullname : {user.first_name} {user.last_name}</div>
        {/* <div className="h7">Developer of web applications, JavaScript, PHP, Java, Python, Ruby, Java, Node.js,
                            etc.
        </div> */}
      </div>
      {/* <ul className="list-group list-group-flush">
        <li className="list-group-item">
          <div className="h6 text-muted">Followers</div>
          <div className="h5">5.2342</div>
        </li>
        <li className="list-group-item">
          <div className="h6 text-muted">Following</div>
          <div className="h5">6758</div>
        </li>
        <li className="list-group-item">Vestibulum at eros</li>
      </ul> */}
    </div>

  )
}

export default ProfileComponent
