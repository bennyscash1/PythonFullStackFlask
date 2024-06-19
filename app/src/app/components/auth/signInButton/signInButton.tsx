import { signInAction } from "@/app/serverActions/auth"

export function SignInButton() {
    return (
        <form
            action={signInAction}
        >
            <button type="submit">Sign In</button>
        </form>
    )
}