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
            <h1 class="text-center align-items-center pb-3 mb-5 w-100">IBJJF Tournaments</h1>
            <table class="table">
                <thead>
                   <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Date</th>
                    <!--th scope="col">IBJJF Id</th-->
                   </tr>
                </thead>
                <tbody>
                  % for event in events:
                    <tr>
                        <td><a href="/events/{{event.get('ibjjfId')}}">{{event.get('name')}}</a></td>
                        <td>{{event.get('date')}}</td>
                        <!--td>{{event.get('ibjjfId')}}</td-->
                    </tr>
                  % end
                </tbody>
            </table>
        </main>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
</html>
