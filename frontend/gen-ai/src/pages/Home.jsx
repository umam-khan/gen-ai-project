// import { Button } from "@/components/ui/button";
// import { UserButton, auth } from "@clerk/nextjs";
// import Link from "next/link";
// import { ArrowRight, LogIn } from "lucide-react";
// import FileUpload from "@/components/FileUpload";
// import { checkSubscription } from "@/lib/subscription";
// import SubscriptionButton from "@/components/SubscriptionButton";
// import { db } from "@/lib/db";
// import { chats } from "@/lib/db/schema";
// import { eq } from "drizzle-orm";
import { Link } from "react-router-dom";
const Home = () => {
  // const { userId } = await auth();
  // const isAuth = !!userId;
  // const isPro = await checkSubscription();
  // let firstChat;
  // if (userId) {
  //   firstChat = await db.select().from(chats).where(eq(chats.userId, userId));
  //   if (firstChat) {
  //     firstChat = firstChat[0];
  //   }
  // }
  return (
    <div className="w-screen min-h-screen bg-gradient-to-r from-rose-100 to-teal-100">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
        <div className="flex flex-col items-center text-center">
          <div className="flex items-center">
            <h1 className="mr-3 text-5xl font-semibold">Chat with medical PDFs</h1>
            {/* <button>login</button> */}
          </div>

          {/* <div className="flex mt-2">
            
            
              <>
                
                  <button>
                    Go to Chats 
                  </button>
              </>
          </div> */}

          <p className="max-w-xl mt-1 text-lg text-slate-600">
            Join millions of students, researchers and professionals to instantly
            answer questions and understand research with AI
          </p>

          <div className="w-full mt-4">
            {/* {isAuth ? (
              <FileUpload />
            ) : ( */}
              <Link to="/main">
                <button className="btn-default">
                   get Started!
                  {/* <LogIn className="w-4 h-4 ml-2" /> */}
                </button>
              </Link>
            {/* )} */}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;