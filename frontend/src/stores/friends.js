import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../composables/useApi'

export const useFriendsStore = defineStore('friends', () => {
  const friends = ref([])
  const requests = ref([])

  async function fetchFriends() {
    const res = await api.get('/friends')
    friends.value = res.data
  }

  async function fetchRequests() {
    const res = await api.get('/friends/requests')
    requests.value = res.data
  }

  async function addFriend(userId) {
    const res = await api.post(`/friends/${userId}`)
    await fetchFriends()
    return res.data
  }

  async function acceptFriend(userId) {
    await api.put(`/friends/${userId}`)
    await fetchRequests()
    await fetchFriends()
  }

  async function removeFriend(userId) {
    await api.delete(`/friends/${userId}`)
    friends.value = friends.value.filter((f) => f.id !== userId)
  }

  async function getFriendStatus(userId) {
    const res = await api.get(`/friends/status/${userId}`)
    return res.data
  }

  return { friends, requests, fetchFriends, fetchRequests, addFriend, acceptFriend, removeFriend, getFriendStatus }
})
