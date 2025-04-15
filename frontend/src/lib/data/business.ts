import createClient from "openapi-fetch";
import type { components, paths } from "../../openapi";

const client = createClient<paths>()

export type ProgramClientScheme = components["schemas"]["ProgramClientScheme"]

const tokenStorageKey = "business_token"
export function getToken() {
    return localStorage.getItem(tokenStorageKey)
}

client.use({
    async onRequest({ request }) {
        const token = getToken()
        if (!token)
            return undefined
        request.headers.set("Authorization", `Bearer ${token}`)
        return request;
    }
})

export async function login(email: string, password: string) {
    const { data, error } = await client.POST("/api/business/login", { body: { email, password }})
    if (error)
        return null
    localStorage.setItem(tokenStorageKey, data.token!)
    return data.token!
}

export async function regsiter(email: string, password: string, name: string, description: string, location: string) {
    const { data, error } = await client.POST("/api/business/register", { body: { email, password, name, description, location }})
    if (error)
        return null
    localStorage.setItem(tokenStorageKey, data.token!)
    return data.token!
}

export async function checkQr(content: string) {
    const { data } = await client.POST("/api/business/check_id", { body: { token: content } })
    return data ?? null
}

export async function redeem(qr: string) {
    const { error } = await client.POST("/api/business/redeem_id", { body: { token: qr } })
    return !error
}

export async function getStats() {
    const { data } = await client.GET("/api/statistics/business")
    return data ?? null
}

export async function createProgram(name: string, target: number, reward: string, maxClaims: number) {
    const { error } = await client.POST("/api/programs/create", { body: { name, target, reward, max_claims: maxClaims, type: "reward" } })
    return !error
}

export async function updateAvatar(file: File) {
    const body = new FormData()
    body.set("file", file)
    const { error } = await client.POST("/api/business/info/image", {
        // @ts-expect-error openapi-typescipt doesnt support files
        body: { file },
        bodySerializer: (body) => {
            const formData = new FormData();
            // @ts-expect-error openapi-typescipt doesnt support files
            formData.set('file', body.file);
            return formData;
        }
    })
    return !error
}
