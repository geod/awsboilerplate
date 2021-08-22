## Roadmap

(unsorted)
1. Evaluate a design change to make the react build self-mutating
2. Integration with cognito to have a full user account setup
3. Currently you can run locally or after registering a domain. I believe it is possible to run it without creating a domain.
It would involve additional complexity of somehow passing the API gateway address to React (it creates a dependency 
between the dynamic infrastructure creation stage and react).
4. It is very easy to add beta then prod (potentially add more sophisticated rolling deployment)
5. The setup is relatively easy but could probably be scripted
6. Better cloudwatch configuration
7. In AWS native the developer experience is the console. Logs are a pain to navigate to. One idea would be to build a simple developer experience. 
However, I suspect this would end up being complex and fragile
8. Build badges
9. Google analytics integration (solve more setup pain)
10. Integrate with a design theme
11. Add more sub patterns ()