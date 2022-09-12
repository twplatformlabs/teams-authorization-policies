# Authorization Policies for Teams API

<div align="center">
	<p>
		<img alt="Thoughtworks Logo" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/thoughtworks_flamingo_wave.png?sanitize=true" width=200 />
    <br />
		<img alt="DPS Title" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/EMPCPlatformStarterKitsImage.png" width=350/>
	</p>
  <h3>Platform Starter Kit v1/teams api</h3>
  <h1>lab-api-teams</h1>
  <a href="https://app.circleci.com/pipelines/github/ThoughtWorks-DPS/teams-authorization-policies"><img src="https://circleci.com/gh/ThoughtWorks-DPS/teams-authorization-policies.svg?style=shield"></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/github/license/ThoughtWorks-DPS/teams-authorization-policies"></a>
</div>
<br />


## Deployment Flow

Styra prefers a GitOps like flow of having branches per environment. This can cause issues as branches get in and out of sync,
 with humans pushing to random branches. Therefore, though we follow that flow, CircleCI orchestrates the merging of branches and should
 be the only thing pushing to those branches. The systems are created as "read-only" meaning they are not changeable in the Styra UI.

 All development happens on `main`. On `push`, linting and testing occurs, and then CCI updates the dev branch with the content of main,
 and ensures the dev system exists in Styra, tracking the dev branch. On `tag`, CCI begins the release process, ensuring systems are 
 created for each environment and then syncing the appropriate branch that the system tracks (QA -> Prod)

### Testing

`opa fmt --diff policy/`

`opa check policy/`

`opa test -v policy/`
