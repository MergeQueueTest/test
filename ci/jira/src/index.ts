import * as core from "@actions/core";
import * as github from "@actions/github";
import JiraApi from "jira-client";
import { EventPayloads } from "@octokit/webhooks";

async function run() {
  try {
    core.debug("Starting PR Title check for Jira Issue Key");
    var issue_ids = extractJiraIssueId(getPullRequestTitle());
    var jira = new JiraApi({
      protocol: "https",
      host: core.getInput('jira-host'),
      username: core.getInput('jira-username'),
      password: core.getInput('jira-api-token'),
      apiVersion: "2",
      strictSSL: true,
    });

    for (var issue_id of issue_ids) {
      await jira
        .findIssue(issue_id)
        .then((e) => {
          console.log(`Found Valid ID ${issue_id} in PR Title`);
        })
        .catch((err) => {
          console.log(err)
          core.setFailed(
            `Found ID ${issue_id} in PR Title but ${issue_id} is NOT a Valid ID`
          );
        });
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

export function getPullRequestTitle() {
  let pull_request = github.context.payload.pull_request;
  core.debug(
    `Pull Request: ${JSON.stringify(github.context.payload.pull_request)}`
  );
  if (pull_request == undefined || pull_request.title == undefined) {
    throw new Error("This action should only be run with Pull Request Events");
  }
  return pull_request.title;
}

function reverse(s: string) {
  return s.split("").reverse().join("");
}

export function extractJiraIssueId(pr_title: string) {
  var jira_matcher = /\d+-[A-Z]+(?!-?[a-zA-Z]{1,10})/g;
  pr_title = reverse(pr_title);
  var m = pr_title.match(jira_matcher);

  // Also need to reverse all the results!
  if (m == null) return [];

  for (var i = 0; i < m.length; i++) {
    m[i] = reverse(m[i]);
  }
  return m.reverse();
}

export async function isValidIssue(issue_id: string, jira_client: JiraApi) {
  jira_client
    .findIssue(issue_id)
    .then(() => {
      return true;
    })
    .catch(() => {
      return false;
    });
}

run()
