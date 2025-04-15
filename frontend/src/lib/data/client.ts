import createClient from "openapi-fetch"
import type { paths } from "../../openapi"

const client = createClient<paths>()

const tokenStorageKey = "client_token"
export function getToken() {
    return localStorage.getItem(tokenStorageKey)
}

async function _createProfile() {
    const { data, error } = await client.POST("/api/clients/new")
    creationPromise = null
    if (error)
        throw new Error(`Failed to create profile: ${error}`)
    return data.token!
}

let creationPromise: Promise<string> | null = null
export async function createProfile() {
    if (creationPromise)
        return creationPromise
    creationPromise = _createProfile()
    return creationPromise
}

export async function getOrCreateToken() {
    const savedToken = getToken()
    if (savedToken)
        return savedToken
    const newToken = await createProfile()
    localStorage.setItem(tokenStorageKey, newToken)
    return newToken
}

export async function logout() {
    const newToken = await createProfile()
    localStorage.setItem(tokenStorageKey, newToken)
}

client.use({
    async onRequest({ schemaPath, request }) {
        if (schemaPath === "/api/clients/new")
            return undefined
        const token = await getOrCreateToken()
        request.headers.set("Authorization", `Bearer ${token}`)
        return request;
    },
    async onResponse({ response }) {
        if (response.status === 401)
            await logout()
    }
})

export async function getProfile() {
    const { data, error } = await client.GET("/api/clients/profile")
    if (error)
        throw new Error(`Failed to get profile: ${error}`)
    return data
}

export async function getQrCodeData() {
    const { data, error } = await client.GET("/api/clients/get_id")
    if (error)
        throw new Error(`Failed to get QR: ${error}`)
    return data
}

export async function getPrograms() {
    const { data, error } = await client.GET("/api/clients/get_programs")
    if (error)
        throw new Error(`Failed to get programs: ${error}`)
    return data ?? []
}

export async function login(email: string, password: string) {
    const { data } = await client.POST("/api/clients/login", { body: { email, password } })
    if (data)
        localStorage.setItem(tokenStorageKey, data.token!)
    return data?.token ?? null
}

export async function regsiter(
    email: string,
    password: string,
    name: string,
    age: number,
    location: string,
    gender: string
) {
    const { error } = await client.PATCH(
        "/api/clients/profile", 
        { body: { email, password, name, age, location, gender } }
    )
    return !error
}
