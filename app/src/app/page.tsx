'use server';

import { useEffect, useState } from "react"
import { auth, signOut } from '../../auth'
import { Session } from "next-auth";
import { SignOutButton } from "./components/auth/signOutButton/signOutButton";
import { SignInButton } from "./components/auth/signInButton/signInButton";

const Home = async () => {
    const authSession = await auth();


    return (
        <div>
            <h1>Home</h1>
            <p>Session: {authSession?.user?.email}</p>
            <SignOutButton />
            <SignInButton />
        </div>
    )
}

export default Home