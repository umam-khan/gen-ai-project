import React from 'react'
import FrameComponent from "../components/FrameComponent";
import botimg from "../assets/bot1@2x.png"
import vector from "../assets/Vector.svg"
const MainHomeInterface = () => {
    return (
      <div className="w-full relative flex flex-row items-start justify-start tracking-[normal] overflow-x-hidden">
        <main className="flex-1 bg-white overflow-hidden flex flex-col items-start justify-start pt-[15px] px-[26px] pb-[130px] box-border relative gap-[125px] max-w-full text-left text-[24px] text-white font-inter mq450:gap-[31px_125px] mq450:pb-[55px] mq450:box-border mq1050:gap-[62px_125px] mq1050:pt-5 mq1050:pb-[84px] mq1050:box-border">
          {/* <div className="relative font-light inline-block min-w-[80px] z-[1] mq450:text-[19px]">
            v English
          </div> */}
          <div className="flex flex-row items-start justify-start pt-0 px-[71px] pb-[77px] box-border max-w-full text-[96px] mq1050:pl-[35px] mq1050:pr-[35px] mq1050:box-border">
            <h3 className="m-0 relative text-inherit font-black font-inherit text-transparent !bg-clip-text [background:linear-gradient(92.47deg,_#fff,_#d3ebfe)] [-webkit-background-clip:text] [-webkit-text-fill-color:transparent] z-[1] mq450:text-10xl mq1050:text-[48px]">
              <p className="m-0">Customer Service</p>
              <p className="m-0">ChatBot</p>
            </h3>
          </div>
          <FrameComponent />
          <header className="w-full h-[563px] absolute !m-[0] top-[0px] right-[0px] left-[0px]">
            <img
              className="absolute top-[0px] left-[0px] w-[1728px] h-[563px] object-cover"
              alt=""
              src={botimg}
            />
            <img
              className="absolute top-[26.7px] left-[118px] w-4 h-[9.5px] z-[1]"
              loading="lazy"
              alt=""
              src={vector}
            />
          </header>
        </main>
      </div>
    )
}
const BhashiniPage = () => {
    return (
      <>
      <MainHomeInterface />
      </>
    )
  }
export default BhashiniPage