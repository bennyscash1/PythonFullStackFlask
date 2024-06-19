import { signOutAction } from "@/app/serverActions/auth"

export function SignOutButton() {
    return (
        <form
            action={signOutAction}
        >
            <button type="submit">Sign Out</button>
        </form>
    )
}