KITT4SME VIQE
-------------
> Scrapping too many parts? Better call VIQE!

Deep learning image processing by Rovimatica to inspect and evaluate
the quality of manufacturing parts.


### Hacking

Install Python (`>= 3.8`), Poetry (`>=1.1`) and the usual Docker
stack (Engine `>= 20.10`, Compose `>= 2.1`). If you've got Nix, you
get a dev shell with the right Python and Poetry versions simply by
running

```console
$ nix shell github:c0c0n3/kitt4sme.viqe?dir=nix
```

Otherwise, install the usual way you do on your platform. Then clone
this repo, `cd` into its root dir and install the Python dependencies

```console
$ git clone https://github.com/c0c0n3/kitt4sme.viqe.git
$ cd kitt4sme.viqe
$ poetry install
```

Finally drop into a virtual env shell to hack away

```bash
$ poetry shell
$ charm .
# ^ Pycharm or whatever floats your boat
```

Run all the test suites:

```console
$ pytest tests
```

or just the unit tests

```console
$ pytest tests/unit
```

Measure global test coverage and generate an HTML report

```console
$ coverage run -m pytest -v tests
$ coverage html
```

Run the VIQE cloud service locally on port 8000

```console
$ poetry shell
$ python -m viqe.main
# ^ same as: uvicorn viqe.main:app --host 0.0.0.0 --port 8000
```

Build and run the Docker image

```console
$ docker build -t kitt4sme/viqe .
$ docker run -p 8000:8000 kitt4sme/viqe
```


### Live simulator

We've whipped together a test bed to simulate a live environment similar
to that of the KITT4SME cluster. In the `tests/sim` directory, you'll find
a Docker compose file with

* Quantum Leap with a CrateDB backend
* Our VIQE service
* KITT4SME Dazzler configured with dashboards to display VIQE's
  inspection reports

To start the show, run (Ctrl+C to stop)

```console
$ poetry shell
$ python tests/sim
```

This will bring up the Docker compose environment (assuming you've
got a Docker engine running already) and simulate the VIQE client
sending an inspection report batch to the VIQE service. On receiving
the batch, the VIQE service splits into two sets of NGSI entities.
(Raw materials and tweezers inspection entities, have a look at the
`viqe.ngsy` module for the data model details.) Then it stashes the
two sets away in Quantum Leap. And here's what's actually going on
under the bonnet:

![Live simulator.][dia.sim]

In fact, if you browse to the CrateDB Web UI at:

- http://localhost:4200.

you should be able to query both the raw materials and tweezers
inspection entity tables to see how the VIQE client inspections
produced by the simulator get transformed into NGSI entities and
then saved to the DB. Now browse to the VIQE Dazzler dashboards
at:

- http://localhost:8080/dazzler/rovi/-/raw_materials/
- http://localhost:8080/dazzler/rovi/-/tweezers/

Each dashboard comes with an explanation of what it is and how it
works. To plot the inspection data in the batch the simulator sent,
choose a time interval spanning from ten hours ago to now, then hit
the load button. (NGSI entities get a UTC-0 timestamp, so you've got
to select a wide enough interval to cater for your time zone, otherwise
the underlying query returns no data.)

Notice that all those entities belong to a tenant named `rovi`. So
you should be able to see Quantum Leap using a separate DB/schema for
that tenant. Also the tenant's name is part of each Dazzler dashboard
URL and is also shown on the dashboard. (KITT4SME relies on this arrangement
to silo tenant data and enforce security policies.)




[dia.sim]: ./viqe-sim.svg
