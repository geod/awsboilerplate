import { CheckCircleFill, Check } from 'react-bootstrap-icons';


function Features() {

  const front_end_features = ["React-Redux (based on React-Boilerplate)", "React Bootstrap 5.0", "React Bootstrap Icons", "Basic Theme", "Fast Local Development"];
  const back_end_features = ["Lambdas (common patterns)", "API Gateway (api.yourdomain)", "Domain Name (Route 53)", "Cloudfront", "Naked Domain Redirect", "All DNS Records"];
  const devops_features = ["All components wired together", "Full Self-mutating CICD Pipeline", "React Build and Deploy", "All Infrastructure Defined in CDK", "Local Development with SAM", "Fully AWS Native", "Fully Customizable"];

  function gen_features(features) {
    return features.map((feature) => <li className="mb-2"><Check/>{feature}</li>);
  };

   return (
            <section className="bg-white py-5" >
                <div className="container" id="features">
                  <div className="text-center mb-5">
                        <h1 className="fw-bolder">Features</h1>
                        <p className="lead fw-normal text-muted mb-0">Contains this site together with back end infrastructure and pipeline <br/>Everything you need, already built, wired together, ready to get started</p>
                    </div>
                  <div className="row gx-5 justify-content-center">
                    <div className="col-lg-6 col-xl-4 text-center">
                      <ul className="list-unstyled mb-4">
                        <li className="mb-2">
                          <strong>Front End</strong>
                        </li>
                        {gen_features(front_end_features)}
                      </ul>
                    </div>
                    <div className="col-lg-6 col-xl-4 text-center">
                      <ul className="list-unstyled mb-4">
                        <li className="mb-2">
                          <strong>Back End & Infrastructure</strong>
                        </li>
                        {gen_features(back_end_features)}
                      </ul>
                    </div>
                    <div className="col-lg-6 col-xl-4 text-center">
                      <ul className="list-unstyled mb-4">
                        <li className="mb-2">
                          <strong>Dev Ops</strong>
                        </li>
                        {gen_features(devops_features)}
                      </ul>
                    </div>
                  </div>
                </div>
            </section>
   )
 }

export default Features;
