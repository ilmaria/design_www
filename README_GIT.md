# [Setup](../../) | [Development](README_DEV.md) | [Git Guide](README_GIT.md)

## Coding a new feature
If you use your git GUI client to do these steps, then you can ignore the commands written
in here. 

1. First pull latest changes from `master` branch.

        git checkout master
        git pull

2. Start a new branch with a name of the new feature. For example, `time-log-button`.

        git checkout -b <new-branch-name>

3. Code your new feature.

4. Commit your code with a short, descriptive commit message. For example,
`Added time log button to dashboard view`. If your changes aren't yet finished but you want to
save it on GitHub, you can add "(WIP)" to your commit message to inform others that the commit
is work in progress. For example, `Added time log button to dashboard view (WIP)`.

        git add -A
        git commit -m "Your commit message"

5. Push changes to remote branch with same branch name. In our example the remote
branch would also be called `time-log-button`.

        git push -u origin <new-branch-name>

6. When the feature is finished, merge the master branch to your feature branch and fix any
merge conflicts. Commit and push your fixed branch to remote repo.

        git merge master
    
   If the merge failed, you have to fix merge conflicts and commit your changes.

        git add -A
        git commit -m "Your commit message"

   Push your final code to the repository. 

        git push

7. Finally got to <https://github.com/ilmaria/design_www> and click "New pull request".
Select your branch and make a pull request.

8. Go to first step.

---

### [> Setup instructions](README.md)
### [> Development instructions](README_DEV.md)
