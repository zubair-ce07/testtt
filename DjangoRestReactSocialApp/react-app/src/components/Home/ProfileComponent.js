import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import EasyEdit from 'react-easy-edit'

import { updateUser } from 'store/modules/user/user.action'

import { resolveImageUrl, toast } from 'helpers/common'

export const ProfileComponent = props => {
  const dispatch = useDispatch()
  const user = useSelector(state => state.user.user)
  const [bio, bioChange] = useState()

  useEffect(() => {
    bioChange(user.bio ? user.bio : 'Write about your self')
  }, [user.bio])

  const saveBio = (value) => { updateProfile({ bio: value }); bioChange(value) }
  const uploadImage = (file) => { updateProfile({ image: file }) }

  const updateProfile = (profile) => {
    dispatch(updateUser(profile)).then((res) => {
      if (res.value.data.status) {
        toast('success', 'Profile Updated Successfully')
      } else {
        toast('success', 'Error while updating profile')
      }
    })
  }

  const cancel = () => { }
  return (
    <div className="card">
      <div className="row">
        <div className="col-md-12">
          <div className="circle">
            {user.image ? <img className="profile-pic" src={resolveImageUrl(user.image)} alt="Profile"/>

              : <i className="fa fa-user fa-5x"></i> }
          </div>
          <div className="p-image">
            <i className="fa fa-camera upload-button"></i>
            <input id='uploadImage' className="file-upload" onChange={(event) => {
              uploadImage(event.currentTarget.files[0])
            }} type="file" accept="image/*"/>
          </div>
        </div>
      </div>
      <div className="card-body profile-card">
        <div className="h5">@{user.username}</div>
        <div className="h7 text-muted">Fullname : {user.first_name} {user.last_name}</div>

      </div>
      <ul className="list-group list-group-flush">
        <div className="h5">Bio</div>
        <li className="list-group-item">
          <EasyEdit type="text" value={bio} onSave={saveBio} onCancel={cancel} saveButtonLabel="Save"
            cancelButtonLabel="Cancel" attributes={{ name: 'bio', id: 1, value: { bio } }}
          />
        </li>
      </ul>
    </div>

  )
}

export default ProfileComponent
