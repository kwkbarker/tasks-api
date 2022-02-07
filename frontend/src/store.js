import { createStore } from 'vuex'
import  createPersistedState from 'vuex-persistedstate'

// module: tasks
const tasks = {
    namespaced: true,

    state() {
        return {
            user: null,
            username: null,
            token: null
        }
    },

    mutations: {

        setUser(state, id) {
            state.user = id
        },

        setUsername(state, username) {
            state.username = username
        },

        setToken(state, token) {
            state.token = token
        },

        logoutUser(state) {
            state.user = null
            state.token = null
            state.username = null
        }

    },

    actions: {

    },

    getters: {

        getUserId(state) {
            return state.user
        },

        getCurrentToken(state) {
            return state.token
        },

        getUsername(state) {
            return state.username
        }

    }
}

export const store = createStore({
    modules: {
        tasks
    },
    plugins: [createPersistedState()]
})