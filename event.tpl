<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>IBJJF Tournament Helper</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  </head>
  <body>
    <div class="col-lg-8 mx-auto p-4 py-md-5">
        <header class="d-flex align-items-center pb-3 mb-5 border-bottom"><a href="/">All IBJJF Tournaments</a></header>
        <main>
            <h1 class="text-center align-items-center pb-3 mb-2 w-100">{{event.get('name')}}</h1>
            <h4 class="text-center pb-3 mb-5">{{event.get('date')}}</h4>
            <table class="table">
                <thead>
                   <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Gender</th>
                    <th scope="col">Belt</th>
                    <th scope="col">Age Division</th>
                    <th scope="col">Weight Class</th>
                    <th scope="col">Bracket</th>
                    <th scope="col">Flo Grappling</th>
                   </tr>
                </thead>
                <tbody>
                  % for athlete in athletes:
                    <tr>
                        <td>{{athlete.get('name')}}</td>
                        <td>{{athlete.get('gender')}}</td>
                        <td>{{athlete.get('belt')}}</td>
                        <td>{{athlete.get('age')}}</td>
                        <td>{{athlete.get('weightclass')}}</td>
                        % if athlete.get('bracket'):
                            <td><a href="{{athlete.get('bracket')}}">link</a></td>
                        % else:
                            <td>-</td>
                        % end
                        % if athlete.get('flolink'):
                            <td><a href="{{athlete.get('flolink')}}">link</a></td>
                        % else:
                            <td>-</td>
                        % end
                    </tr>
                  % end
                </tbody>
            </table>
        </main>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
</html>
