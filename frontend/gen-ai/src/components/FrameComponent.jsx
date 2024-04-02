import { useCallback } from "react";
import seller1 from "../assets/seller1.png"
import buyer1 from "../assets/buyer1.png"
import { Link } from "react-router-dom";
const FrameComponent = () => {
  const onGroupContainerClick = useCallback(() => {
    // Please sync "MacBook Pro 16" - 2" to the project
  }, []);

  const onGroupContainer1Click = useCallback(() => {
    // Please sync "MacBook Pro 16" - 2" to the project
  }, []);

  return (
    <section className="self-stretch flex flex-row items-start justify-center max-w-full text-center text-17xl text-darkslateblue font-inter">
      <div className="w-[1262px] flex flex-col items-end justify-start gap-[4px] max-w-full">
        <div className="self-stretch h-[62px] flex flex-col items-start justify-start gap-[17px]">
          <div className="self-stretch flex flex-row items-start justify-center py-0 pr-[21px] pl-5">
            <div className="w-[301px] relative font-semibold inline-block mq450:text-3xl mq1050:text-10xl">
              What’s your role?
            </div>
          </div>
          <img
            className="self-stretch h-px relative max-w-full overflow-hidden shrink-0"
            loading="lazy"
            alt=""
            src="/line-1.svg"
          />
        </div>
        <div className="mt-10 w-[1242px] flex flex-row items-start justify-end py-0 px-[77px] box-border max-w-full text-45xl text-black lg:pl-[38px] lg:pr-[38px] lg:box-border">
          <div className="flex-1 flex flex-row items-end justify-between max-w-full gap-[20px] lg:flex-wrap lg:justify-center">
            <div
              className="w-[486px] flex flex-row items-start justify-start min-w-[486px] max-w-full cursor-pointer lg:flex-1 mq750:min-w-full"
              onClick={onGroupContainerClick}
            >
              <div className="h-[350px] flex-1 relative max-w-full">
                <div className="absolute top-[77px] left-[0px] rounded-lg [background:linear-gradient(74.81deg,_#34373c,_#4e5f73)] w-[486px] h-[273px]" />
                <div className="absolute top-[0px] left-[32px] w-[422px] h-[338px] flex flex-row items-end justify-center py-[88px] px-5 box-border bg-cover bg-no-repeat bg-[top] max-w-full z-[1]"
                style={{ backgroundImage: `url(${seller1})` }}>
                  <img
                    className="h-[338px] w-[422px] relative object-cover hidden max-w-full"
                    alt=""
                    src={seller1}
                  />
                  <div className="w-[187px] flex flex-row items-start justify-start">
                    <div className="flex-1 relative font-black [text-shadow:0px_0px_12px_rgba(0,_0,_0,_0.45)] [filter:blur(40px)] z-[2] mq450:text-19xl mq1050:text-32xl">
                      Seller
                    </div>
                    <div className="w-[187px] relative font-black text-white inline-block [text-shadow:0px_0px_12px_rgba(0,_0,_0,_0.6)] z-[3] ml-[-187px] mq450:text-19xl mq1050:text-32xl">
                      Seller
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <Link to="/audio2">
            <div
              className="h-[321px] w-[506px] relative min-w-[506px] max-w-full cursor-pointer lg:flex-1 mq750:min-w-full"
              onClick={onGroupContainer1Click}
            >
              <div className="absolute top-[48px] left-[0px] rounded-lg [background:linear-gradient(74.81deg,_#34373c,_#4e5f73)] w-[486px] h-[273px]" />
              <div className="absolute top-[0px] left-[97px] w-[409px] h-[300px] flex flex-row items-end justify-start py-[79px] px-[51px] box-border bg-cover bg-no-repeat bg-[top] max-w-full z-[1]"
     style={{ backgroundImage: `url(${buyer1})` }}>
  <img
    className="h-[300px] w-[409px] relative object-cover hidden max-w-full"
    alt=""
    src={buyer1}
  />
  <div className="w-[189px] flex flex-row items-start justify-start">
    <div className="flex-1 relative font-black [text-shadow:0px_0px_12px_rgba(0,_0,_0,_0.45)] [filter:blur(40px)] z-[2] mq450:text-19xl mq1050:text-32xl">
      Buyer
    </div>
    <div className="flex-1 relative font-black text-white [text-shadow:0px_0px_12px_rgba(0,_0,_0,_0.45)] z-[3] ml-[-189px] mq450:text-19xl mq1050:text-32xl">
      Buyer
    </div>
  </div>
</div>
            </div>
            </Link>
          </div>
        </div>
      </div>
    </section>
  )
}
export default FrameComponent